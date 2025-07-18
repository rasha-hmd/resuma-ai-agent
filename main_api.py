from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
import os, json, re, subprocess
from tempfile import NamedTemporaryFile
from database.db import init_db, SessionLocal
from database.models import ResumeSubmission

from agents.evaluator import get_evaluator_agent
from agents.editor import get_editor_agent
from agents.strategist import should_continue
from agents.cover_letter import get_cover_letter_agent
from utils.convert_pdf_to_json import extract_resume_json
from utils.render_resume import render_resume_to_tex
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from rulebased.main_rulebased import ResumeJobMatcher
from fastapi import File
from fastapi.responses import JSONResponse


# ----------- Init DB -----------
init_db()
app = FastAPI()
matcher = ResumeJobMatcher()

# ----------- frontend -----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------- Helpers -----------
def extract_json(text):
    match = re.search(r"\{[\s\S]*\}", text)
    return match.group(0) if match else None

def compile_latex_to_pdf(tex_path: str, output_dir: str):
    subprocess.run(
        ["pdflatex", "-output-directory", output_dir, tex_path],
        check=True
    )
# ----------- Upload Endpoint -----------
@app.post("/upload/")
async def upload_resume(
    resume_file: UploadFile,
    job_description: str = Form(...)
):
    print("📥 Upload received:", resume_file.filename)
    # Save uploaded resume temporarily
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(await resume_file.read())
        resume_path = tmp.name
    print("✅ Saved resume to", resume_path)

    output_dir = "data/output"
    os.makedirs(output_dir, exist_ok=True)

    # Parse resume into JSON
    resume_json = extract_resume_json(resume_path)
    print("🔍 Extracted resume JSON")
    resume_str = json.dumps(resume_json, indent=2)
    edited_resume_str = resume_str

    # First evaluation
    evaluator_output = get_evaluator_agent(job_description, resume_str)
    print("🧠 Evaluator output:", evaluator_output[:200], "...")
    json_str = extract_json(evaluator_output)
    if not json_str:
        return {"error": "Failed to extract evaluation JSON"}

    try:
        parsed_output = json.loads(json_str)
    except json.JSONDecodeError as e:
        return {"error": "Evaluation output was not valid JSON", "details": str(e)}

    evaluation = parsed_output.get("evaluation", {})
    course_recs = parsed_output.get("course_recommendations", [])
    # Save evaluation.json
    with open(os.path.join(output_dir, "evaluation.json"), "w", encoding="utf-8") as f:
        json.dump(evaluation, f, indent=2)

    # Save course_recommendations.json if available
    if course_recs:
        with open(os.path.join(output_dir, "course_recommendations.json"), "w", encoding="utf-8") as f:
            json.dump(course_recs, f, indent=2)

    # Evaluation & Editing loop
    iteration = 1
    max_iterations = 4

    while iteration <= max_iterations:
        should_continue_loop, rating = should_continue(evaluation)

        if not should_continue_loop:
            break

        edited_resume_str = get_editor_agent(
            original_resume_str=resume_str,
            edited_resume_str=edited_resume_str,
            feedback=json.dumps(evaluation, indent=2)
        )

        reevaluation_output = get_evaluator_agent(job_description, edited_resume_str)
        json_str = extract_json(reevaluation_output)
        if not json_str:
            break

        try:
            feedback = json.loads(json_str)
            evaluation = feedback.get("evaluation", {})
        except json.JSONDecodeError:
            break

        iteration += 1

    # Save final resume
    resume_final_data = json.loads(edited_resume_str)
    resume_final_path = os.path.join(output_dir, "resume_final.json")
    with open(resume_final_path, "w", encoding="utf-8") as f:
        f.write(edited_resume_str)

    # Generate LaTeX
    tex_path = os.path.join(output_dir, "resume_final.tex")
    render_resume_to_tex(resume_final_data, output_path=tex_path)

    # Generate Cover Letter
    cover_letter_agent = get_cover_letter_agent()
    cover_letter = cover_letter_agent.invoke({
        "job_description": job_description,
        "resume": edited_resume_str
    })
    cover_letter_path = os.path.join(output_dir, "cover_letter.txt")
    with open(cover_letter_path, "w", encoding="utf-8") as f:
        f.write(cover_letter)

    # Read contents from generated files
    with open(tex_path, "r", encoding="utf-8") as f:
        latex_content = f.read()

    with open(cover_letter_path, "r", encoding="utf-8") as f:
        cover_letter_text = f.read()

    compile_latex_to_pdf("data/output/resume_final.tex", "output_data")

    # Save to SQLite
    db = SessionLocal()
    submission = ResumeSubmission(
        resume_filename=resume_file.filename,
        job_description=job_description,
        latex_path=tex_path,
        latex_content=latex_content,
        cover_letter_path=cover_letter_path,
        cover_letter_text=cover_letter_text,
        evaluation_json=json.dumps(evaluation, indent=2),
        course_recommendations=json.dumps(course_recs, indent=2)
    )
    app.mount("/data", StaticFiles(directory="data"), name="data")

    db.add(submission)
    db.commit()
    db.refresh(submission)
    print("✅ All processing complete. Returning final result.")
    return {
        "message": "Processing complete!",
        "submissionId": submission.id,
        "resumeTex": tex_path,
        "coverLetter": cover_letter,
        "evaluation": evaluation,
        "courseRecommendations": course_recs
    }


# ----------- List Submissions Endpoint -----------
@app.get("/submissions/")
def list_submissions():
    db = SessionLocal()
    submissions = db.query(ResumeSubmission).all()
    return [
        {
            "id": s.id,
            "resume_filename": s.resume_filename,
            "latex_path": s.latex_path,
            #"latex_content": s.latex_content,
            "cover_letter_path": s.cover_letter_path,
            #"cover_letter_text": s.cover_letter_text,
            "job_description": s.job_description,
            "evaluation": s.evaluation_json,
            #"course_recommendations": s.course_recommendations
        }
        for s in submissions
    ]


@app.get("/download-resume")
def download_resume():
    pdf_path = "data/output/resume_final.pdf"
    if os.path.exists(pdf_path):
        return FileResponse(pdf_path, media_type="application/pdf", filename="resume_final.pdf")
    return {"error": "PDF not found"}

@app.get("/download/final_resume_json")
def download_final_resume_json():
    file_path = os.path.join("data", "output", "resume_final.json")
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename="final_resume.json",
            media_type="application/json"
        )
    return {"error": "Final resume JSON not found"}

@app.get("/download/final_resume_pdf")
def download_final_resume_pdf():
    file_path = os.path.join("data", "output", "resume_final.pdf")
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename="final_resume.pdf",
            media_type="application/pdf"
        )
    return {"error": "Final resume PDF not found"}


@app.get("/output/cover_letter.txt")
def get_cover_letter():
    file_path = os.path.join("data", "output", "cover_letter.txt")
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename="cover_letter.txt", media_type="text/plain")
    return {"error": "Cover letter not found"}

# ----------- Rule Based -----------
@app.post("/rulebased")
async def rule_based_match(resume_file: UploadFile = File(...), job_file: UploadFile = File(...)):
    resume_path = f"temp_{resume_file.filename}"
    job_path = f"temp_{job_file.filename}"

    with open(resume_path, "wb") as f:
        f.write(await resume_file.read())
    with open(job_path, "wb") as f:
        f.write(await job_file.read())

    try:
        results = matcher.analyze_match(resume_path, job_path)
        os.remove(resume_path)
        os.remove(job_path)

        match_results = results['match_results']

        # Convert sets to lists before returning JSON
        category_results = {}
        for cat, data in match_results['category_results'].items():
            category_results[cat] = {
                'score': data['score'],
                'weighted_score': data['weighted_score'],
                'matched': list(data['matched']),   # convert set to list
                'missing': list(data['missing']),   # convert set to list
                'total_job_keywords': data['total_job_keywords']
            }

        response = {
            "weighted_score": match_results['weighted_score'],
            "simple_score": match_results['simple_score'],
            "category_results": category_results,
            "overall_matched": list(match_results['overall_matched']),  # convert set to list
            "overall_missing": list(match_results['overall_missing']),  # convert set to list
            "recommendation": None  # Optional, you can add logic for recommendation if you want
        }

        # Optionally add recommendation logic here based on weighted_score
        if response["weighted_score"] >= 70:
            response["recommendation"] = "Strong match! This resume aligns well with the job requirements."
        elif response["weighted_score"] >= 50:
            response["recommendation"] = "Good potential. Consider highlighting missing key skills."
        else:
            response["recommendation"] = "Significant gaps. Focus on developing missing technical skills."

        return JSONResponse(content=response)

    except Exception as e:
        return {"error": str(e)}

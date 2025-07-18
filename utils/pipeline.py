from agents.evaluator import get_evaluator_agent
from agents.editor import get_editor_agent
from agents.strategist import should_continue
from agents.cover_letter import get_cover_letter_agent
from utils.convert_pdf_to_json import extract_resume_json
from utils.render_resume import render_resume_to_tex
import json, os

def process_resume_and_job(resume_pdf_path, job_description):
    resume_json = extract_resume_json(resume_pdf_path)  # Your CV parser
    resume_str = json.dumps(resume_json, indent=2)

    evaluation_output = get_evaluator_agent(job_description, resume_str)
    evaluation = json.loads(evaluation_output)["evaluation"]

    if should_continue(evaluation)[0]:
        edited = get_editor_agent(resume_str, resume_str, json.dumps(evaluation, indent=2))
        resume_str = edited

    try:
        if isinstance(resume_str, str):
            final_resume_data = json.loads(resume_str)
        else:
            final_resume_data = resume_str  # it's already a dict
    except json.JSONDecodeError as e:
        print("❌ Failed to parse edited resume JSON:", e)
        print("🔍 Raw edited resume string:", resume_str)
        raise

    tex_path = "data/output/resume_final.tex"
    render_resume_to_tex(final_resume_data, output_path=tex_path)

    # 📝 Save cover letter
    cover_letter_agent = get_cover_letter_agent()
    cover_letter = cover_letter_agent.invoke({
        "job_description": job_description,
        "resume": resume_str
    })
    with open("data/output/cover_letter.txt", "w", encoding="utf-8") as f:
        f.write(cover_letter)

    # 🧪 Save evaluation JSON
    with open("data/output/evaluation.json", "w", encoding="utf-8") as f:
        json.dump(evaluation, f, indent=2)

    return tex_path, cover_letter, evaluation

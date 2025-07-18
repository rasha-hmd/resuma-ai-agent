import json
import os
import re

from agents.evaluator import get_evaluator_agent
from agents.editor import get_editor_agent
from agents.strategist import should_continue
from agents.cover_letter import get_cover_letter_agent
from utils.render_resume import render_resume_to_tex


# ----------- Helpers -----------
def extract_json(text):
    """Extract the first valid JSON object from a string using regex."""
    match = re.search(r"\{[\s\S]*\}", text)
    return match.group(0) if match else None

# ----------- Paths -----------

INPUT_DIR = "data/input"
OUTPUT_DIR = "data/output"

# ----------- Load input -----------

with open(os.path.join(INPUT_DIR, "resume.json"), "r", encoding="utf-8") as f:
    resume_json = json.load(f)

with open(os.path.join(INPUT_DIR, "job_desc.txt"), "r", encoding="utf-8") as f:
    job_description = f.read()

# ----------- First Evaluation -----------

print("🔍 Running Evaluation Agent...")
evaluator_output = get_evaluator_agent(job_description, json.dumps(resume_json, indent=2))

# 🧪 Print raw output for debug
print("\n🧾 Raw Output from Evaluator Agent:\n")
print(evaluator_output)

# Extract and parse JSON
json_str = extract_json(evaluator_output)

if not json_str:
    print("❌ Could not extract JSON from the output.")
    exit(1)

try:
    parsed_output = json.loads(json_str)
    print("✅ Successfully parsed JSON!")
except json.JSONDecodeError as e:
    print("❌ ERROR: Could not parse evaluator JSON output.")
    print("Reason:", e)
    print("Extracted Output:\n", json_str)
    exit(1)

# ----------- Save evaluation & courses -----------

evaluation = parsed_output.get("evaluation", {})
course_recs = parsed_output.get("course_recommendations", [])

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(os.path.join(OUTPUT_DIR, "evaluation.json"), "w", encoding="utf-8") as f:
    json.dump(evaluation, f, indent=2)

with open(os.path.join(OUTPUT_DIR, "course_recommendations.json"), "w", encoding="utf-8") as f:
    json.dump(course_recs, f, indent=2)

# ----------- Evaluation Loop -----------

resume_str = json.dumps(resume_json, indent=2)
edited_resume_str = resume_str
iteration = 1
max_iterations = 4  # Set max iterations to prevent infinite loop

while iteration <= max_iterations:
    print(f"\n🔁 Iteration {iteration}: Checking resume rating...")
    should_continue_loop, rating = should_continue(evaluation)
    print(f"⭐ Current resume rating: {rating}/10")

    if not should_continue_loop:
        print("✅ Resume is good enough! Proceeding to finalization.")
        break

    print("✍️ Running Resume Editor Agent...")
    edited_resume_str = get_editor_agent(
        original_resume_str=resume_str,
        edited_resume_str=edited_resume_str,
        feedback=json.dumps(evaluation, indent=2)
    )

    print("🔁 Re-evaluating the edited resume...")
    reevaluation_output = get_evaluator_agent(job_description, edited_resume_str)

    json_str = extract_json(reevaluation_output)
    if not json_str:
        print("❌ Could not extract JSON during iteration.")
        break

    try:
        feedback = json.loads(json_str)
        evaluation = feedback.get("evaluation", {})
    except json.JSONDecodeError:
        print("❌ ERROR: Could not parse evaluator JSON in iteration.")
        break

    iteration += 1
else:
    print(f"⚠️ Maximum iterations ({max_iterations}) reached. Stopping editing loop.")

# ----------- Save Final Resume (JSON + LaTeX) -----------

resume_final_path = os.path.join(OUTPUT_DIR, "resume_final.json")
with open(resume_final_path, "w", encoding="utf-8") as f:
    f.write(edited_resume_str)

# Convert string back to dict for LaTeX rendering
resume_final_data = json.loads(edited_resume_str)

print("🖨️ Generating LaTeX resume...")
render_resume_to_tex(resume_final_data, output_path=os.path.join(OUTPUT_DIR, "resume_final.tex"))
print("✅ LaTeX resume saved at data/output/resume_final.tex")


# ----------- Generate Cover Letter -----------

print("\n✉️ Generating cover letter...")
cover_letter_agent = get_cover_letter_agent()
cover_letter = cover_letter_agent.invoke({
    "job_description": job_description,
    "resume": edited_resume_str
})

with open(os.path.join(OUTPUT_DIR, "cover_letter.txt"), "w", encoding="utf-8") as f:
    f.write(cover_letter)

print("\n✅ All done! Outputs saved in 'data/output/'.")

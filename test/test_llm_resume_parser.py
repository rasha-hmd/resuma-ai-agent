from utils.convert_pdf_to_json import extract_resume_json

pdf_path = "C:/Users/lenovo/Desktop/resuma_agents/data/input/testResume.pdf"

print("🔍 Parsing resume using LLaMA 3...")
output = extract_resume_json(pdf_path)

print("\n🧾 LLM Output:")
print(output)

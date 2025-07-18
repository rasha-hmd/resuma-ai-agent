import os
from jinja2 import Environment, FileSystemLoader
import json

def render_resume_to_tex(resume_data, output_path="data/output/resume_final.tex"):
    if isinstance(resume_data, str):
        try:
            resume_data = json.loads(resume_data)
        except Exception as e:
            print("❌ resume_data was string and couldn't be parsed:", resume_data)
            raise

    templates_dir = r"C:\Users\lenovo\Desktop\resuma_agents\templates"
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("resume_template.tex")

    print("🔍 resume_data type:", type(resume_data))
    rendered_tex = template.render(**resume_data)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered_tex)

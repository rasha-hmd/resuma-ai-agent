import os
import json
from utils.render_resume import render_resume_to_tex

# Small sample JSON resume
resume_data = {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "linkedin_username": "janedoe",
    "skills": {
        "Programming": ["Python", "JavaScript"],
        "DevOps": ["Docker", "AWS"]
    },
    "experience": [
        {
            "company": "TechCorp",
            "date": "2022 - 2023",
            "title": "Junior Python Developer",
            "location": "Remote",
            "bullets": [
                "Built REST APIs with Flask",
                "Integrated AWS services"
            ]
        }
    ],
    "education": [
        {
            "institution": "Some University",
            "startDate": "2018",
            "endDate": "2022",
            "degree": "B.Sc. Computer Science",
            "location": "USA"
        }
    ],
    "projects": [
        {
            "title": "CloudSync",
            "description": "A tool for syncing files to AWS S3."
        }
    ],
    "certifications": [
        {
            "name": "AWS Certified Developer",
            "date": "2023-05"
        }
    ]
}

# Output path
output_path = "data/output/test_resume.tex"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Render to LaTeX
render_resume_to_tex(resume_data, output_path=output_path)

print(f"LaTeX resume saved to: {output_path}")

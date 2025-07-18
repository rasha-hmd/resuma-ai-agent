# 📄 Resuma: AI-Powered Resume Agent

Resuma is an AI-powered resume assistant that helps job seekers effortlessly tailor their resumes and cover letters to specific job descriptions. It leverages the LLaMA 3 language model (via Ollama), intelligent rule-based analysis, and course recommendation logic to enhance your resume, generate a tailored cover letter, and recommend upskilling resources — all from a simple web interface.

> ✨ Powered by FastAPI, LangChain, SQLite, React, Tailwind, and LLaMA 3 via Ollama.

---

## 🚀 Features

- 🔍 Upload Resume (PDF) + Job Description (TXT)
- 🤖 LLM-based Resume Evaluator with LangChain + LLaMA 3
- 📝 Intelligent Resume Editing to Match the Job
- 📬 Auto-generated Tailored Cover Letter
- 📚 Personalized Course Recommendations (from resume gap analysis)
- 📊 Rule-based Matching Engine with Score & Keyword Breakdown
- 📥 Download LaTeX Resume & Cover Letter
- 📁 Admin Dashboard to Browse All Submissions
- 🐳 Fully Containerized with Docker & Docker Compose

---

## 📦 Tech Stack

| Layer             | Technology Used               |
|------------------|-------------------------------|
| Frontend         | React + Tailwind CSS          |
| Backend API      | FastAPI                       |
| LLM Integration  | LangChain + Ollama (LLaMA 3)  |
| Resume Parsing   | PyMuPDF + LLM JSON Extraction |
| Resume Rendering | LaTeX + Jinja2                |
| DB Storage       | SQLite                        |
| Containerization | Docker, Docker Compose        |

---

## 📸 Screenshots

![Home page]
![Results page]
![Cover letter]
![Suggested courses]
![Rule based]

---

## 🧠 LLM Architecture

- Prompt templates for resume evaluation, editing, and cover letter generation are stored under `/prompts`.
- LangChain pipelines call local LLaMA 3 models via Ollama.
- Agents:
  - `evaluator`: Analyzes strengths, gaps, and relevance.
  - `editor`: Tailors resume by rewriting JSON sections.
  - `cover_letter`: Generates a job-specific cover letter.
  - `strategist`: Decides whether to re-evaluate or finalize.

---

## 🛠️ Local Development

### 1. Prerequisites

- Python 3.10+
- Node.js & npm
- Docker & Docker Compose
- [Ollama](https://ollama.com/) (with llama3 model pulled)

```bash
ollama pull llama3
```

### 2. Run with Docker Compose

Make sure your root has this structure:

```
resuma-ai-agent/
resuma_agents/             # Project Root
│
├── agents/                # LLM agents: evaluator, editor, strategist, etc.
├── data/                  # Input/output files (PDFs, JSONs, etc.)
├── database/              # DB models and initialization scripts
├── frontend/              # React frontend (Vite project)
├── prompts/               # LLM prompt templates for each agent
├── resuma/                # Library root or main package (can hold core logic)
├── rulebased/             # Rule-based resume-job matcher
├── templates/             # LaTeX and HTML templates (e.g., resume rendering)
├── test/                  # Unit and integration tests
├── utils/                 # Utility functions (PDF parsing, keyword extraction, etc.)
│
├── .gitignore             # Git ignored files config
├── docker-compose.yml     # Docker services config
├── Dockerfile.backend     # Dockerfile for the FastAPI backend
├── main.py                # Local dev script (no API)
├── main_api.py            # FastAPI backend entrypoint
├── requirements.txt       # Python dependencies
└── resuma.db              # SQLite database file (auto-generated)


```

Then run:

```bash
docker-compose up --build
```

App will be available at:

- Frontend: http://localhost:5173
- Backend: http://localhost:8000

---

## 🧪 API Endpoints

| Method | Route                     | Description                             |
|--------|---------------------------|-----------------------------------------|
| POST   | `/optimize`               | LLM resume analysis + enhancement       |
| POST   | `/generate_cover_letter`  | Generate job-specific cover letter      |
| POST   | `/rulebased`              | Rule-based keyword matching + scoring   |
| GET    | `/download/latex_resume`  | Download final LaTeX resume             |
| GET    | `/download/cover_letter`  | Download generated cover letter         |
| GET    | `/submissions`            | List all processed submissions          |

---

## 📂 Database Schema (SQLite)

- Table: `ResumeSubmission`
  - id (int)
  - original_resume_path
  - optimized_resume_path
  - original_resume_json
  - optimized_resume_json
  - cover_letter
  - course_recommendations (JSON)
  - job_description

---

## 👩‍💻 Contributions

This project was developed by Rasha Hammoud and Faten Mortada as part of the Mini Project course at the Lebanese University - Faculty of Engineering III.

---


## 📜 License

MIT License. Feel free to fork, modify, and share!
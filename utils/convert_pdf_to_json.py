import fitz  # PyMuPDF
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
import os

prompt_path = os.path.join(os.path.dirname(__file__), "..", "prompts", "resume_parser_prompt.txt")
prompt_path = os.path.abspath(prompt_path)

def extract_resume_text(pdf_path):
    """Extract raw text from a PDF file using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text

def extract_resume_json(pdf_path):
    """Use LLaMA 3 to convert resume PDF content into structured JSON."""
    # Step 1: Extract plain text from PDF
    resume_text = extract_resume_text(pdf_path)

    # Step 2: Load the parsing prompt
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_template = f.read()

    # Step 3: Create LangChain pipeline with the prompt and LLaMA model
    prompt = PromptTemplate(
        input_variables=["resume_text"],
        template=prompt_template
    )

    llm = OllamaLLM(model="llama3", temperature=0.3)
    chain = prompt | llm

    # Step 4: Generate structured JSON output
    structured_json = chain.invoke({"resume_text": resume_text})
    return structured_json

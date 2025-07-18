from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate


def get_evaluator_agent(job_description, resume_json_str):
    # Load the updated prompt (with course recs) from file
    with open("prompts/evaluator_prompt.txt", "r", encoding="utf-8") as f:
        template = f.read()

    prompt = PromptTemplate(
        input_variables=["job_description", "resume"],
        template=template
    )

    llm = OllamaLLM(model="llama3", temperature=0.3, base_url="http://ollama:11434")
    chain = prompt | llm

    # Run the chain with inputs and return the raw JSON string output
    return chain.invoke({
        "job_description": job_description,
        "resume": resume_json_str
    })

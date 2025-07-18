from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate


def get_cover_letter_agent():
    with open("prompts/cover_letter_prompt.txt", "r", encoding="utf-8") as f:
        prompt_template = f.read()

    prompt = PromptTemplate(
        input_variables=["job_description", "resume"],
        template=prompt_template
    )

    llm = OllamaLLM(model="llama3", temperature=0.3, base_url="http://ollama:11434")
    chain = prompt | llm

    return chain

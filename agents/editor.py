from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate

def get_editor_agent(original_resume_str, edited_resume_str, feedback):
    with open("prompts/editor_prompt.txt", "r", encoding="utf-8") as f:
        template = f.read()

    prompt = PromptTemplate(
        input_variables=["original", "edited", "feedback"],
        template=template
    )
    llm = OllamaLLM(model="llama3", temperature=0.3, base_url="http://ollama:11434")
    chain = prompt | llm

    return chain.invoke({
        "original": original_resume_str,
        "edited": edited_resume_str,
        "feedback": feedback
    })

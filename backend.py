import fitz  # PyMuPDF
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def summarize_pdf(pdf_path):
    input_text = extract_text_from_pdf(pdf_path)

    model = OllamaLLM(model="llama3.2:3b")

    system_template = "Summarize the following text, the summary should include all the important points"
    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_template), ("user", "{Text}")]
    )

    prompt = prompt_template.invoke({"Text": input_text})
    response = model.invoke(prompt)
    return response

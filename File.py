# Ensure that PyMuPDF is correctly installed and imported
try:
    import fitz  # PyMuPDF
except ModuleNotFoundError as e:
    print("PyMuPDF is not installed. Please install it using 'pip install PyMuPDF'")
    raise e

from langchain import OpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text

# Initialize LangChain
api_key = "your_openai_api_key"  # Replace with your OpenAI API key
llm = OpenAI(api_key=api_key)
prompt_template = PromptTemplate(input_variables=["text"], template="Analyze the following text: {text}")
chain = LLMChain(llm=llm, prompt=prompt_template)

# Function to analyze text with LangChain
def analyze_text_with_langchain(text):
    result = chain.run({"text": text})
    return result

# Main script
pdf_path = "example.pdf"  # Replace with your PDF file path

# Extract text from PDF
text = extract_text_from_pdf(pdf_path)
print("Extracted Text:", text)

# Analyze the extracted text
result = analyze_text_with_langchain(text)
print("Analysis Result:", result)

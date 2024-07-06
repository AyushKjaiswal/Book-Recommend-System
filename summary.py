from PyPDF2 import PdfReader
from langchain_community.llms import Ollama
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader


def map_reduce(file_path):
    try:
        # Provide the path of the PDF file
        pdfreader = PdfReader(file_path)
        
        # Read text from the PDF
        text = ''
        for i, page in enumerate(pdfreader.pages):
            content = page.extract_text()
            if content:
                text += content

        llm = Ollama(model="llama3")

        # Split the text into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=20)
        chunks = text_splitter.create_documents([text])
        
        # Load the summarization chain and summarize the text
        chain = load_summarize_chain(llm, chain_type='map_reduce', verbose=False)
        summary = chain.invoke(chunks)
        
        return summary['output_text']
    except Exception as e:
        return f"An error occurred: {e}"





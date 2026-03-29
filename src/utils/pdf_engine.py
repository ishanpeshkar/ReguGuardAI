import os
from pypdf import PdfReader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger

class PDFProcessingEngine:
    def __init__(self):
        # Gemini Embeddings
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, # Gemini handles larger chunks well
            chunk_overlap=200
        )

    def extract_text(self, pdf_path: str) -> str:
        logger.info(f"Extracting text from: {pdf_path}")
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text

    def create_vector_store(self, text: str, store_name: str):
        if not os.path.exists("data/vector_stores"):
            os.makedirs("data/vector_stores")
            
        chunks = self.text_splitter.split_text(text)
        vector_store = FAISS.from_texts(chunks, self.embeddings)
        vector_store.save_local(f"data/vector_stores/{store_name}")
        logger.success(f"Vector store {store_name} created.")
        return vector_store
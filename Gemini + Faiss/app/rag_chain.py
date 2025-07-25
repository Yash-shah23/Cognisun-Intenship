# rag_chain.py
# app/rag_chain.py

import os
import logging
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PDF_PATH = "app/data/ifrs-inr-press-release.pdf"
DB_FAISS_PATH = "app/db"

def load_faiss_index():
    logger.info("📄 Loading FAISS index from disk...")
    if os.path.exists(DB_FAISS_PATH):
        return FAISS.load_local(DB_FAISS_PATH, HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"), allow_dangerous_deserialization=True)
    else:
        logger.info("📄 Creating new FAISS index from PDF")
        loader = PyPDFLoader(PDF_PATH)
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=250)
        texts = splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(texts, embeddings)
        vectorstore.save_local(DB_FAISS_PATH)
        return vectorstore

# Initialize FAISS index only once
vectorstore = load_faiss_index()

def get_rag_response(query: str, lang: str = "en") -> str:
    logger.info("📥 Starting RAG pipeline...")

    retriever = vectorstore.as_retriever()
    llm = ChatGroq(
        groq_api_key=os.getenv("GROQ_API_KEY"),
        model_name="llama3-70b-8192"
    )
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    result = qa_chain.invoke(query)
    logger.info("✅ RAG response complete.")
    return result["result"]

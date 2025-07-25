import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import RetrievalQA

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
DATA_DIR = "data"
FAISS_DIR = "faiss_store"

def load_documents():
    documents = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DATA_DIR, filename))
            documents.extend(loader.load())
    return documents

def create_vectorstore():
    docs = load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=250)
    docs = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings()
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(FAISS_DIR)

def get_rag_chain():
    if not os.path.exists(FAISS_DIR):
        create_vectorstore()

    embeddings = HuggingFaceEmbeddings()
    db = FAISS.load_local(FAISS_DIR, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever()
    llm = GoogleGenerativeAI(
        model="gemini-1.5-flash", temperature=0.2, google_api_key=GOOGLE_API_KEY
    )
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

qa_chain = get_rag_chain()

def get_rag_answer(question: str) -> str:
    return qa_chain.invoke({"query": question})["result"]

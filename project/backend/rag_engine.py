import os
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_ollama import OllamaLLM
from file_loader import load_file_content

DB_PATH = "vectorstore/db"
EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
embedding_model = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
llm = OllamaLLM(model="gemma:2b")
vectordb = None

def load_and_embed(file_path):
    global vectordb
    docs = load_file_content(file_path)
    chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)
    vectordb = FAISS.from_documents(chunks, embedding_model)
    vectordb.save_local(DB_PATH)

def get_qa_chain():
    global vectordb
    if vectordb is None:
        vectordb = FAISS.load_local(DB_PATH, embedding_model)
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=False)

def handle_structured_csv_question(file_path: str, question: str) -> str | None:
    try:
        df = pd.read_csv(file_path, encoding='cp1252', dtype=str).fillna("")
        q_lower = question.lower()

        if "gender" in q_lower and "average" in q_lower and "stay" in q_lower:
            df["Length_of_Stay"] = pd.to_numeric(df["Length_of_Stay"], errors='coerce')
            avg = df.groupby("Gender")["Length_of_Stay"].mean().dropna().to_dict()
            return f"Average Length of Stay by Gender: {avg}"

        # Add more rules below...
        return None
    except Exception as e:
        return f"CSV parsing failed: {str(e)}"

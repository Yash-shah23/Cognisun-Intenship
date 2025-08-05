import os
from langchain_community.document_loaders import PyPDFLoader # Used to load PDF documents
from langchain_community.vectorstores import FAISS # FAISS for storing and retrieving embeddings
from langchain_huggingface import HuggingFaceEmbeddings # HuggingFace model for generating embeddings
from langchain.chains import RetrievalQA # High-level chain for question answering
from langchain_groq import ChatGroq # Groq's LLM integration
from langchain.prompts import PromptTemplate # Used to create custom prompts
from langchain.text_splitter import RecursiveCharacterTextSplitter # Splits large text into smaller chunks
from bson import ObjectId
from db import sessions
from config import DATA_PATH, VECTORSTORE_DIR, VECTORSTORE_PATH, EMBEDDING_MODEL



# from langchain_community.document_loaders import (
#     PyPDFLoader, 
#     CSVLoader,       # ✅ for CSV files
#     JSONLoader,      # ✅ for JSON files
#     UnstructuredWordDocumentLoader  # ✅ for Word files
# )


# Cache FAISS index and memory
vectorstore = None

def embed_documents_once():
    """
    Load existing FAISS index if available, otherwise 
    read PDFs, create embeddings, and save FAISS index.
    """
    if os.path.exists(VECTORSTORE_PATH):
        print("✅ Using existing FAISS index...")
        return FAISS.load_local(
            VECTORSTORE_DIR,
            HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL),
            allow_dangerous_deserialization=True
        )

    print("🔄 Creating FAISS index for the first time...")

    documents = []
    for file in os.listdir(DATA_PATH):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DATA_PATH, file))
            documents.extend(loader.load())


        # elif file.endswith(".csv"):
        #     loader = CSVLoader(file_path)
        # elif file.endswith(".json"):
        #     loader = JSONLoader(file_path, jq_schema='.')  
        # elif file.endswith(".docx") or file.endswith(".doc"):
        #     loader = UnstructuredWordDocumentLoader(file_path)
        # else:
        #     print(f"⚠️ Unsupported file type: {file}. Skipping...")
        #     continue  

    
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=400)
    texts = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vs = FAISS.from_documents(texts, embeddings)

    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    vs.save_local(VECTORSTORE_DIR)
    print("✅ FAISS index created and saved.")

    return vs

# ✅ Initialize FAISS once
vectorstore = embed_documents_once()

def get_rag_response(query: str, session_id: str) -> str:
    """Retrieve context-aware answer using FAISS + Groq LLM."""
    print(f"📌 Generating RAG response for session: {session_id}")

    retriever = vectorstore.as_retriever(
        search_type="mmr",  # ✅ Avoids redundant chunks
        search_kwargs={"k": 15, "fetch_k": 20}
    )

    prompt = PromptTemplate(
        template=(
            "You are a professional AI assistant.\n\n"
            "### Context:\n{context}\n\n"
            "### Question:\n{question}\n\n"
            "### Instructions:\n"
            "- Answer **only** from the context.\n"
            "- Combine related facts into a single, concise, well-structured answer.\n"
            "- Use short paragraphs, bullet points, and **bold** for key info.\n"
            "- If answer is missing, reply exactly:\n"
            "⚠️ Sorry, but the provided content does not contain information about the question you asked.\n\n"
            "### Answer:"
        ),
        input_variables=["context", "question"]
    )


    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatGroq(model="llama3-70b-8192", temperature=0),
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain.run(query)

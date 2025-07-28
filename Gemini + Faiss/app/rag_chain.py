import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- Configuration Paths ---
DATA_PATH = "data"                   # Directory where PDFs are stored
VECTORSTORE_DIR = "vectorstore"       # Directory to store FAISS index
VECTORSTORE_PATH = os.path.join(VECTORSTORE_DIR, "index.faiss")

# Global variable to store FAISS vectorstore
vectorstore = None


def embed_documents_once():
    """
    Loads existing FAISS index if available; otherwise,
    reads all PDFs, creates embeddings, and saves the FAISS index.
    """
    # ✅ If index already exists, reuse it to save time
    if os.path.exists(VECTORSTORE_PATH):
        print("✅ Using existing FAISS index...")
        return FAISS.load_local(
            VECTORSTORE_DIR,
            HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
            allow_dangerous_deserialization=True
        )

    print("🔄 Creating FAISS index for the first time...")

    # ✅ Load all PDF documents
    documents = []
    for file in os.listdir(DATA_PATH):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DATA_PATH, file))
            documents.extend(loader.load())

    # ✅ Split documents into smaller chunks for better retrieval
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = splitter.split_documents(documents)

    # ✅ Generate embeddings using HuggingFace model
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    # ✅ Create FAISS vectorstore
    vs = FAISS.from_documents(texts, embeddings)

    # ✅ Save FAISS index to disk
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    vs.save_local(VECTORSTORE_DIR)
    print("✅ FAISS index created and saved.")
    
    return vs


# ✅ Initialize FAISS only once on server startup
vectorstore = embed_documents_once()


def get_rag_response(query: str) -> str:
    """
    Retrieves the most relevant context using FAISS
    and generates an answer using Groq's LLM.
    """
    # ✅ Create retriever for searching similar document chunks
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

  

    # ✅ Strict prompt to avoid hallucinations
    prompt = PromptTemplate(
        template=(
            "You are an AI assistant.\n"
            "Use ONLY the provided context to answer.\n"
            "If no relevant context is found, still try to respond politely or give a basic greeting.\n\n"
            "Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        ),
        input_variables=["context", "question"]
    )

    # ✅ Create RetrievalQA chain with prompt
    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatGroq(model="llama3-8b-8192", temperature=0), # Use Groq's LLaMA3 model
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )

    # ✅ Get the final answer
    return qa_chain.run(query)

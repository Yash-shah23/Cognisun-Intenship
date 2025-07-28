import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter

DATA_PATH = "data"
VECTORSTORE_DIR = "vectorstore"
VECTORSTORE_PATH = os.path.join(VECTORSTORE_DIR, "index.faiss")

# Global variable to store the loaded FAISS vectorstore
vectorstore = None

def embed_documents_once():
    """Embed PDFs only if FAISS index is not already created."""
    if os.path.exists(VECTORSTORE_PATH):
        print("✅ Using existing FAISS index...")
        return FAISS.load_local(
            VECTORSTORE_DIR,
            HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
            allow_dangerous_deserialization=True
        )

    print("🔄 Creating FAISS index for the first time...")

    documents = []
    for file in os.listdir(DATA_PATH):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(DATA_PATH, file))
            documents.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vs = FAISS.from_documents(texts, embeddings)

    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    vs.save_local(VECTORSTORE_DIR)
    print("✅ FAISS index created and saved.")
    return vs

# Initialize FAISS once when server starts
vectorstore = embed_documents_once()

def get_rag_response(query: str) -> str:
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    llm = ChatGroq(model="llama3-8b-8192", temperature=0)

    # ✅ Updated prompt to strictly avoid hallucinations
    prompt = PromptTemplate(
        template=(
            "You are an AI assistant. "
            "Use ONLY the provided context to answer. "
            "If the context is not relevant to the question, "
            "reply exactly with: 'I cannot answer this question based on the provided document.'\n\n"
            "Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        ),
        input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain.run(query)

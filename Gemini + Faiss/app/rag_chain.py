import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from bson import ObjectId
from db import sessions
from config import DATA_PATH, VECTORSTORE_DIR, VECTORSTORE_PATH, EMBEDDING_MODEL

# Cache FAISS index and memory
vectorstore = None
memory_dict = {}

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
#
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=250)
    texts = splitter.split_documents(documents)

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vs = FAISS.from_documents(texts, embeddings)

    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    vs.save_local(VECTORSTORE_DIR)
    print("✅ FAISS index created and saved.")

    return vs

# ✅ Initialize FAISS once
vectorstore = embed_documents_once()

def get_memory(session_id: str):
    """Retrieve or initialize session memory."""
    if session_id not in memory_dict:
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        session = sessions.find_one({"_id": ObjectId(session_id)})
        if session and "messages" in session:
            for msg in session["messages"]:
                if msg["role"] == "user":
                    memory.chat_memory.add_user_message(msg["text"])
                elif msg["role"] == "bot":
                    memory.chat_memory.add_ai_message(msg["text"])

        memory_dict[session_id] = memory

    return memory_dict[session_id]

def get_rag_response(query: str, session_id: str) -> str:
    """Retrieve context-aware answer using FAISS + Groq LLM."""
    print(f"📌 Generating RAG response for session: {session_id}")

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    prompt = PromptTemplate(
        template=(
            "You are an AI assistant.\n"
            "Answer the question ONLY using the provided context.\n"
            "If the context is not relevant, say exactly:\n"
            "'I cannot answer this question based on the provided document.'\n\n"
            "Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        ),
        input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=ChatGroq(model="llama3-8b-8192", temperature=0),
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain.run(query)

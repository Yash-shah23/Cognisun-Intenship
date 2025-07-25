from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings  # ✅ new

from langchain_ollama import OllamaLLM  # ✅ NEW
from langchain.chains import RetrievalQA
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import time

load_dotenv()

app = FastAPI()

# ✅ CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Connect to MongoDB
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["chatbot"]
chatlog = db["logs"]

# ✅ Load vector store
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db_faiss = FAISS.load_local("vectorstore", embedding, allow_dangerous_deserialization=True)

# ✅ Retrieve more relevant chunks (k=5)
retriever = db_faiss.as_retriever(search_kwargs={"k": 8})

qa = RetrievalQA.from_chain_type(llm=OllamaLLM(model="gemma:2b"), retriever=retriever, verbose=True)


# ✅ Pydantic model
class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Query):
    start = time.time()
    raw_answer = qa.run(q.question).strip()
    if not raw_answer or "I don't know" in raw_answer.lower():
        answer = "Sorry, I don’t know that."
    else:
        answer = raw_answer
    chatlog.insert_one({"question": q.question, "answer": answer})
    print("⏱️ Time taken:", time.time() - start, "seconds")
    return {"answer": answer}

@app.get("/ping-mongo")
def ping_mongo():
    try:
        db.command("ping")
        return {"status": "MongoDB is connected ✅"}
    except Exception as e:
        return {"error": str(e)}

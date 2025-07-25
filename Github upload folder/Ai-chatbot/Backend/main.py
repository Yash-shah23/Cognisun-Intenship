from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings  
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA



app = FastAPI()

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load vector store
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db_faiss = FAISS.load_local("vectorstore", embedding, allow_dangerous_deserialization=True)


retriever = db_faiss.as_retriever(search_kwargs={"k": 3})

qa = RetrievalQA.from_chain_type(llm=OllamaLLM(model="llama3:latest"), retriever=retriever, verbose=True)


# Pydantic model
class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(q: Query):
    raw_answer = qa.run(q.question).strip()
    if not raw_answer or "I don't know" in raw_answer.lower():
        answer = "Sorry, I don’t know that."
    else:
        answer = raw_answer
    return {"answer": answer}

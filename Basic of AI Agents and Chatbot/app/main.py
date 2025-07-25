from fastapi import FastAPI
from pydantic import BaseModel
from rag_chain import build_rag_chain
import uvicorn

app = FastAPI()

# Request schema
class Query(BaseModel):
    question: str

# Load the RAG chain at startup
qa_chain = build_rag_chain()

@app.get("/")
def root():
    return {"message": "RAG API with Gemma 2B and Ollama is running."}

@app.post("/ask")
def ask_q(query: Query):
    answer = qa_chain.run(query.question)
    return {"question": query.question, "answer": answer}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

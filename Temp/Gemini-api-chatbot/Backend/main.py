from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_engine import get_rag_answer

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Question(BaseModel):
    question: str

@app.post("/api/chat")
async def chat(query: Question):
    try:
        answer = get_rag_answer(query.question)
        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}

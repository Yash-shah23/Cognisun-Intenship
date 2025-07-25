# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.rag_chain import get_rag_response
from dotenv import load_dotenv
load_dotenv()
import os 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Allow CORS from frontend (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    lang: str = "en"

@app.post("/ask")
async def ask(request: QueryRequest):
    logger.info("✅ Received /ask POST request")
    logger.info(f"➡️ Query: {request.query}, Lang: {request.lang}")
    answer = get_rag_response(request.query, request.lang)
    logger.info(f"✅ Answer: {answer}")
    return {"answer": answer}

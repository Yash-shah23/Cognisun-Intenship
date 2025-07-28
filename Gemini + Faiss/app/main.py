from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from utils.translation import translate, detect_language
from utils.speech import speech_to_text
from rag_chain import get_rag_response

load_dotenv()
app = FastAPI(title="RAG Chatbot API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str
    selected_lang: str = "en"  # Force language selection

class TextData(BaseModel):
    text: str


@app.post("/ask")
async def ask(data: Query):
    """
    Multilingual RAG chatbot.
    - Always processes in English internally.
    - Translates the final response to selected language (default: English).
    """
    # Detect spoken language (for info) but respect selected_lang
    
    target_lang = data.selected_lang if data.selected_lang else "en"

    # Translate input → English → RAG processing
    translated_query = translate(data.query, target_lang="en")
    english_answer = get_rag_response(translated_query)

    # Translate final answer → selected language
    final_answer = (
        english_answer if target_lang == "en"
        else translate(english_answer, target_lang=target_lang)
    )

    return JSONResponse(content={"answer": final_answer, "lang": target_lang})


@app.post("/speech-to-text")
async def convert_speech(file: UploadFile = File(...)):
    """
    Converts uploaded speech audio into text using speech recognition.
    """
    audio_path = f"temp_{file.filename}"
    
    with open(audio_path, "wb") as f:
        f.write(await file.read())

    try:
        text = speech_to_text(audio_path)
    finally:
        os.remove(audio_path)

    return JSONResponse(content={"text": text})


@app.post("/detect-and-translate")
async def detect_and_translate(data: TextData):
    """
    Detects the language of provided text and ensures proper translation
    before displaying it in the input box.
    """
    text = data.text
    detected_lang = detect_language(text)
    
    corrected_text = (
        translate(text, target_lang=detected_lang)
        if detected_lang != "en"
        else text
    )

    return JSONResponse(content={"corrected_text": corrected_text, "lang": detected_lang})

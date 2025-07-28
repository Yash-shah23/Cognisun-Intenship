from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from utils.translation import translate, detect_language
from utils.speech import speech_to_text
from rag_chain import get_rag_response

# ✅ Load environment variables securely
load_dotenv()

app = FastAPI(title="RAG Chatbot API", version="1.0")

# ✅ Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Request models
class Query(BaseModel):
    query: str

class TextData(BaseModel):
    text: str


@app.post("/ask")
async def ask(data: Query):
    """
    Handles multilingual questions, translates them to English,
    retrieves answers using RAG, and translates the final response
    back to the user's language.
    """

    # Detect the input language
    detected_lang = detect_language(data.query)

    # Translate question to English for RAG processing
    translated_query = translate(data.query, target_lang="en")

    # Get AI response (includes greetings & basic chat)
    english_answer = get_rag_response(translated_query)

    # Translate answer back to user's language if needed
    final_answer = (
        english_answer if detected_lang == "en"
        else translate(english_answer, target_lang=detected_lang)
    )

    return JSONResponse(content={"answer": final_answer, "lang": detected_lang})


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

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
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    query: str

class TextData(BaseModel):
    text: str

@app.post("/ask")
async def ask(data: Query):
    detected_lang = detect_language(data.query)
    translated_query = translate(data.query, target_lang="en")
    english_answer = get_rag_response(translated_query)
    final_answer = (
        english_answer if detected_lang == "en"
        else translate(english_answer, target_lang=detected_lang)
    )
    return JSONResponse(content={"answer": final_answer, "lang": detected_lang})

@app.post("/speech-to-text")
async def convert_speech(file: UploadFile = File(...)):
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
    text = data.text
    detected_lang = detect_language(text)
    corrected_text = (
        translate(text, target_lang=detected_lang)
        if detected_lang != "en"
        else text
    )
    return JSONResponse(content={"corrected_text": corrected_text, "lang": detected_lang})

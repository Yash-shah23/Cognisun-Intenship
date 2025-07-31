from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from dotenv import load_dotenv
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from db import sessions
from utils.translation import translate, detect_language
from utils.speech import speech_to_text
from rag_chain import get_rag_response
from models import Query, TextData, RenameRequest, Message

load_dotenv()
app = FastAPI(title="RAG Chatbot API", version="1.0")

# ✅ Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Create a new chat session
@app.post("/create-session")
async def create_session():
    session = {
        "created_at": datetime.utcnow(),
        "messages": [],
        "session_name": "New Chat",
        "is_deleted": False
    }
    inserted = sessions.insert_one(session)
    return JSONResponse(content={"id": str(inserted.inserted_id)})

@app.put("/delete-session/{session_id}")
async def delete_session(session_id: str):
    """Soft-delete a session."""
    try:
        session_obj_id = ObjectId(session_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid session ID")

    result = sessions.update_one(
        {"_id": session_obj_id, "is_deleted": False},
        {"$set": {"is_deleted": True}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Session not found or already deleted")

    return JSONResponse(content={"message": "Session deleted successfully"})


@app.put("/rename-session/{session_id}")
async def rename_session(session_id: str, body: RenameRequest):
    """Rename a session."""
    try:
        session_obj_id = ObjectId(session_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid session ID")

    result = sessions.update_one(
        {"_id": session_obj_id, "is_deleted": False},
        {"$set": {"session_name": body.new_name}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Session not found or deleted")

    return JSONResponse(content={"message": "Session renamed successfully"})


# ✅ Get all messages of a session
@app.get("/session/{session_id}")
async def get_session_messages(session_id: str):
    try:
        session = sessions.find_one({"_id": ObjectId(session_id), "is_deleted": False})
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")

        messages = session.get("messages", [])
        for msg in messages:
            if "timestamp" in msg:
                msg["timestamp"] = msg["timestamp"].isoformat()

        return JSONResponse(content={"messages": messages})
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid session ID")

# ✅ Get all active sessions
@app.get("/sessions")
async def get_all_sessions():
    sessions_list = []
    for s in sessions.find({"is_deleted": False}):
        sessions_list.append({
            "id": str(s["_id"]),
            "name": s.get("session_name", "New Chat"),
            "created_at": s.get("created_at", datetime.utcnow()).strftime("%Y-%m-%d %H:%M:%S")
        })
    return JSONResponse(content=sessions_list)

@app.post("/ask")
async def ask(data: Query):
    try:
        session_obj_id = ObjectId(data.session_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid session ID")

    session = sessions.find_one({"_id": session_obj_id, "is_deleted": False})
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # ✅ Translate question → English for model understanding
    translated_query = translate(data.query, target_lang="en")
    
    # ✅ Get English answer from RAG
    english_answer = get_rag_response(translated_query, session_id=data.session_id)

    # ✅ Translate bot's answer back to user's selected language
    final_answer = (
        translate(english_answer, target_lang=data.selected_lang)
        if data.selected_lang and data.selected_lang != "en"
        else english_answer
    )

    # ✅ Save messages
    user_msg = Message(role="user", text=data.query).dict()
    bot_msg = Message(role="bot", text=final_answer).dict()

    user_msg["timestamp"] = datetime.utcnow()
    bot_msg["timestamp"] = datetime.utcnow()

    sessions.update_one({"_id": session_obj_id}, {"$push": {"messages": user_msg}})
    sessions.update_one({"_id": session_obj_id}, {"$push": {"messages": bot_msg}})

    return JSONResponse(content={
        "answer": final_answer,
        "lang": data.selected_lang,
        "session_id": data.session_id
    })


# ✅ Speech-to-text conversion
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

# ✅ Detect language and auto-translate
@app.post("/detect-and-translate")
async def detect_and_translate(data: TextData):
    detected_lang = detect_language(data.text)
    corrected_text = translate(data.text, target_lang=detected_lang) if detected_lang != "en" else data.text
    return JSONResponse(content={"corrected_text": corrected_text, "lang": detected_lang})

from pydantic import BaseModel

class Query(BaseModel):
    session_id: str
    query: str
    selected_lang: str = "en"

class Message(BaseModel):
    role: str  # "user" or "bot"
    text: str

class TextData(BaseModel):
    text: str

class RenameRequest(BaseModel):
    new_name: str

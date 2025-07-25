from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from qa_engine import answer_question, update_vector_store
from data_loader import load_file_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_store = {"content": ""}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    content = await load_file_data(file)
    data_store["content"] = content
    background_tasks.add_task(update_vector_store, content)
    return {"message": "File uploaded. Embedding will be ready shortly."}

@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    if not data_store["content"]:
        return {"answer": "Please upload a data file first."}
    answer = answer_question(question)
    return {"answer": answer}

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from rag_engine import load_and_embed, get_qa_chain, handle_structured_csv_question
import shutil, os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)
latest_uploaded_file = None  # 👈 Tracks the last file uploaded


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global latest_uploaded_file
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        load_and_embed(file_path)
        latest_uploaded_file = file_path
        return {"message": "File uploaded and embedded successfully."}
    except Exception as e:
        return {"error": f"Upload failed: {str(e)}"}


@app.post("/ask")
async def ask_question(question: str = Form(...)):
    global latest_uploaded_file
    try:
        if not latest_uploaded_file:
            return {"error": "No file has been uploaded yet."}
        if not question.strip():
            return {"error": "Question is empty."}

        # 👉 Structured CSV Logic
        if latest_uploaded_file.endswith(".csv"):
            csv_result = handle_structured_csv_question(latest_uploaded_file, question)
            if csv_result:
                return {"answer": csv_result}

        # 👉 Default RAG QA Chain
        qa_chain = get_qa_chain()
        result = qa_chain.run(question)
        return {"answer": result}

    except Exception as e:
        return {"error": f"Processing failed: {str(e)}"}

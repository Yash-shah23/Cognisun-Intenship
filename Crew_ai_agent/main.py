from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from db import QA, SessionLocal, init_db
from crew_config import get_crew_agent
import traceback

app = FastAPI()
templates = Jinja2Templates(directory="templates")

init_db()

@app.get("/", response_class=HTMLResponse)
def read_form(request: Request):
    db = SessionLocal()
    history = db.query(QA).all()
    db.close()
    return templates.TemplateResponse("index.html", {"request": request, "history": history})


@app.post("/ask", response_class=HTMLResponse)
def handle_question(request: Request, question: str = Form(...)):
    print("Received question:", question)

    try:
        crew = get_crew_agent()
        result = crew.kickoff(inputs={"input": question})
        print("CrewAI result:", result)
    except Exception as e:
        print("CrewAI Error:")
        traceback.print_exc()
        result = "Sorry, an error occurred while processing your question."

    # Store Q&A in database
    try:
        db = SessionLocal()
        qa = QA(question=question, answer=result)
        db.add(qa)
        db.commit()
        history = db.query(QA).all()
        db.close()
    except Exception as db_err:
        print("DB Error:")
        traceback.print_exc()
        history = []

    return templates.TemplateResponse("index.html", {"request": request, "history": history})

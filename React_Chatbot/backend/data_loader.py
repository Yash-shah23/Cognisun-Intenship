import os
import json
import pandas as pd
import pdfplumber
from qa_engine import update_vector_store

async def load_file_data(file):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = ""
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    elif file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
        text = df.to_string(index=False)
    elif file_path.endswith(".json"):
        data = json.load(open(file_path, "r"))
        text = json.dumps(data, indent=2)
    else:
        text = "Unsupported file type"

    os.remove(file_path)
    update_vector_store(text)
    return text

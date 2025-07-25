import os
import pandas as pd
from langchain.schema import Document
from langchain_community.document_loaders import (
    PyPDFLoader, TextLoader,
    UnstructuredWordDocumentLoader, UnstructuredExcelLoader, UnstructuredHTMLLoader
)

def load_file_content(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".csv":
        df = pd.read_csv(file_path, encoding='cp1252', dtype=str).fillna("")
        rows = df.to_dict(orient="records")
        texts = [" | ".join(f"{k}: {v}" for k, v in row.items()) for row in rows]
        return [Document(page_content="\n".join(texts))]

    loader_map = {
        ".pdf": PyPDFLoader,
        ".txt": TextLoader,
        ".md": TextLoader,
        ".docx": UnstructuredWordDocumentLoader,
        ".xlsx": UnstructuredExcelLoader,
        ".html": UnstructuredHTMLLoader,
        ".htm": UnstructuredHTMLLoader,
    }

    if ext in loader_map:
        return loader_map[ext](file_path).load()
    raise ValueError(f"Unsupported file type: {ext}")

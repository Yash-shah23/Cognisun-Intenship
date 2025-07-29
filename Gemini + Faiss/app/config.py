import os

DATA_PATH = "data"
VECTORSTORE_DIR = "vectorstore"
VECTORSTORE_PATH = os.path.join(VECTORSTORE_DIR, "index.faiss")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

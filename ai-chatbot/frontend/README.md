# 🧠 AI PDF Chatbot using RAG + FAISS + HuggingFace + Ollama (Gemma)

This project is an intelligent chatbot that allows you to ask questions based on pre-defined PDF. It uses **RAG (Retrieval-Augmented Generation)** with **FAISS**, **HuggingFace embeddings**, and **Ollama's Gemma LLM** to return accurate, context-aware answers from the document.

---

## 📁 Project Structure

project-root/
│
├── ingest.py # Loads PDF, splits, embeds, and stores chunks in FAISS
├── main.py # FastAPI backend handling chat requests
├── vectorstore/ # Saved FAISS vector DB
└── index.pdf # Your PDF file


---

## 🚀 How It Works

### ✅ Backend Stack:
- **FastAPI** – RESTful API
- **LangChain** – For RAG and integration
- **FAISS** – Vector database for similarity search
- **HuggingFace** – `all-MiniLM-L6-v2` embeddings
- **Ollama** – LLM backend (`gemma:2b`)


### ✅ Workflow:
1. **Ingestion**: PDF is chunked and embedded → stored in FAISS (`ingest.py`)
2. **Query**: User asks a question → relevant chunks are retrieved → passed to LLM (via Ollama)
3. **Answer**: LLM responds → answer returned to frontend 

---

## ⚙️ Requirements

> Make sure the following tools are installed:

- Python 3.10+
- Node.js (for frontend, if using)
- [Ollama](https://ollama.com/) (for local LLMs)

---

## 📦 Install Dependencies

```bash
# Create & activate virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate # To activate

# Install Python dependencies
pip install -r requirements.txt

Requirements.txt

fastapi
uvicorn
pydantic
python-dotenv
pymongo
langchain
langchain-community
langchain-ollama
sentence-transformers


🧠 Step 1: Ingest PDF
Place your index.pdf file in the root folder, then run: 
python ingest.py

This will:
Load and chunk the PDF
Generate embeddings
Store them in a local FAISS vectorstore (./vectorstore)

🛠️ Step 2: Start Ollama
Run this in new cmd after starting virtual env: 
ollama run gemma:2b

📖 Step 3: start Backend server
Run this in new cmd after starting virtual env: 
 python -m uvicorn main:app --reload 

🧠 Step 4: Start frontend
Run this in new cmd after starting virtual env: 
npm start 

👨‍💻 Author
Built with ❤️ by [Yash Shah]

Screen-shot:
![alt text](C:\Users\USER\Desktop\Yash Shah\Screenshot_Ai_Agent.jpeg)
# 🤖 Simple AI Agent using LangChain + Ollama (Gemma 2B) + RAG

This is a minimal, local **Retrieval-Augmented Generation (RAG)** agent built with LangChain, FAISS, HuggingFace Embeddings, and the **Gemma 2B LLM** running via **Ollama**.

Ask natural-language questions about a plain text file (`docs.txt`) — answers are generated based on context retrieved from that file.

---

## 📁 Project Structure
project-root/
│
├── main.py # FastAPI app with POST endpoint /ask
├── rag_chain.py # Loads, splits, embeds text + builds RAG pipeline
├── docs.txt # Your input knowledge file
├── requirements.txt # Python dependencies

---

## 🧠 What It Does

- Loads `docs.txt` (your knowledge base)
- Splits it into chunks
- Embeds using HuggingFace (`MiniLM`)
- Indexes with FAISS
- Queries via Ollama running `gemma:2b`

---

## ⚙️ Requirements

Install the following:

- Python 3.10+
- [Ollama](https://ollama.com/) (for running `gemma`)
- `docs.txt` file (in root folder)

---

## 📦 Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements.txt

Requirements.txt

fastapi
uvicorn
pydantic
langchain
langchain-community
sentence-transformers


🧠 Step 1: Start Ollama
You must run the Gemma model via Ollama before using the app:

ollama run gemma:2b

🛠️ Step 2: Run the App

uvicorn main:app --reload

📝 Example docs.txt

LangChain is an open-source framework for developing applications powered by language models. It enables easy integration with LLMs, vector databases, and retrieval systems like FAISS.

👨‍💻 Author

Built with ❤️ by [Yash Shah]


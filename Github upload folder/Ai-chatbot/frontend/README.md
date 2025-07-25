# 🤖 AI Chatbot with RAG (FastAPI + FAISS + React)

This is a **simple AI-powered chatbot** built using:

- 🧠 **Retrieval-Augmented Generation (RAG)**
- ⚙️ **FastAPI** for the backend
- 💾 **FAISS** vector search
- 🧬 **HuggingFace Embeddings**
- 💬 **Ollama (Llama3)** as the LLM
- 🎨 **React** for a ChatGPT-like frontend UI

---

## 📂 Project Structure


Ai-chatbot/
├── backend/
│ ├── main.py # FastAPI app
│ ├── ingest.py # RAG chain with FAISS + LLM
│ ├── Test.pdf # Source document for QA
│ ├──requirements.txt
│
├── frontend/
│ ├── src/
│ │ ├── App.jsx # Chat UI logic
│ │ ├── App.css # ChatGPT-style UI
│ │ └── index.js
│ └── package.json
└── README.md


---

## 🛠️ Installation

### 🔧 Backend Setup (FastAPI)

1. Navigate to the backend folder:

    cd backend

2. Create and activate a virtual environment:

    python -m venv venv
    venv\Scripts\activate   # Windows

3. Install all dependencies:

    pip install -r requirements.txt

4. Start the FastAPI server:

    uvicorn main:app --reload

➡️ Server runs at: http://localhost:8000


💻 Frontend Setup (React)
    

1. Exit the backend folder:

    cd ..

2. Make react project

    npm create-react-app frontend 

3. Install React dependencies:

    npm install 

4.  npm start

    npm start 
        # Starts the frontend server 

➡️ App runs at: http://localhost:3000


🔍 How It Works:

    A PDF document (e.g., Test.pdf) is embedded using HuggingFace embeddings.

    FAISS indexes and stores chunks of the document.

    When a user asks a question:

    Relevant chunks are retrieved by FAISS.

    These chunks + the question are passed to Ollama LLM (Llama3).

    The LLM generates an answer based only on the retrieved content.

    If the question is unrelated to the document, it replies with:
    "Provided question is out of context."


✅ This is called RAG (Retrieval-Augmented Generation).

🧪 Test Cases

✅ Valid Questions (From PDF)

Question-->

    Q1.What was Amazon's total revenue in 2023?	
    Q2.What is Project Kuiper?	
    Q3.How much did AWS grow year-over-year?	
    Q4.What are primitives in AWS?	 

❌ Out-of-Context Questions

Question-->	

    Q1.What is quantum physics?	
    "Provided question is out of context."
    
    Q2.Who is Elon Musk?	
    "Provided question is out of context."

    Q3.What is the capital of Canada?	
    "Provided question is out of context."

💡 LLM Behavior

    Model Used: gemma2:9b-instruct-q4_0 via Ollama

    Friendly questions like "hello" or "how are you?" are answered directly by the LLM (fallback when no context is retrieved).

You can change the model by editing this line in rag_engine.py:

   """ OllamaLLM(model="gemma2:9b-instruct-q4_0") """


🚀 Features
    ✅ RAG-based accurate answers

    ✅ Friendly responses for casual messages

    ✅ "Out of context" detection

    ✅ Fast and responsive frontend/backend


🧱 Technologies Used

    Component	Tech Stack
    Backend	FastAPI, LangChain, FAISS
    Embeddings	HuggingFace MiniLM
    LLM	Ollama (gemma2:9b-instruct-q4_0)
    Frontend	React + Axios + CSS


🗃️ Requirements

    Python 3.10+

    Node.js 16+

    Ollama installed and model pulled (ollama pull gemma2:9b-instruct-q4_0)

    Chrome or modern browser


React

📌 Future Improvements (Optional Ideas)

    Upload new files dynamically

    Support multilingual documents

    Use chat history to give better context

    Switch between different models (Mistral, Gemma, GPT-4 etc.)


🧠 What You Learn from This Project:

    🔎 How Retrieval-Augmented Generation (RAG) works

    🧬 How to use HuggingFace embeddings + FAISS

    ⚙️ How to connect FastAPI with LangChain and Ollama




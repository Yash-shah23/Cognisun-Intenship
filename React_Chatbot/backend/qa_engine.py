from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain_ollama import OllamaEmbeddings, OllamaLLM

llm = OllamaLLM(model="gemma:2b")
embedding_model = OllamaEmbeddings(model="gemma:2b")
vector_db = None

def update_vector_store(text: str):
    global vector_db
    try:
        print("📄 Splitting and embedding content...")
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        docs = splitter.split_documents([Document(page_content=text)])
        vector_db = FAISS.from_documents(docs, embedding_model)
        print("✅ Vector DB ready.")
    except Exception as e:
        print(f"❌ Embedding error: {e}")

def answer_question(question: str) -> str:
    global vector_db
    if not vector_db:
        return "Embedding is not ready. Please wait a few seconds after upload."

    try:
        qa = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vector_db.as_retriever(),
            chain_type="stuff"
        )
        result = qa.run(question)
        if not result or "i don't know" in result.lower():
            return "Sorry, I couldn’t find an answer in the document."
        return result.strip()
    except Exception as e:
        print(f"❌ QA Error: {e}")
        return "Sorry, there was a problem processing your question."

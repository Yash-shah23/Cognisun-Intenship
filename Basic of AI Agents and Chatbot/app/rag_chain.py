from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA

def build_rag_chain():
    # Load knowledge base
    loader = TextLoader("docs.txt")
    documents = loader.load()

    # Split text into chunks
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    # Embed and index
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(docs, embeddings)
    retriever = vectordb.as_retriever()

    # Local Gemma model via Ollama (2B model)
    llm = Ollama(model="gemma:2b")

    # RAG pipeline
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

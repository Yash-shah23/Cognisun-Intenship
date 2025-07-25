from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings  
from langchain_ollama import OllamaLLM 

# Load PDF
loader = PyPDFLoader("Test.pdf")
docs = loader.load()

# Chunking
splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=250)
chunks = splitter.split_documents(docs)

# Use fast Hugging Face model
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create vector store
db = FAISS.from_documents(chunks, embedding)

# Save
db.save_local("vectorstore")
print(f"Vectorstore saved with {len(chunks)} chunks!")

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from embeddings.local_embedding_model import LocalEmbeddingModel

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "medical_docs")
DATA_DIR = os.path.abspath(DATA_DIR)
INDEX_DIR = "medical-rag/vectorstore/faiss_index"

def load_documents():
    docs = []
    for file in os.listdir(DATA_DIR):
        path = os.path.join(DATA_DIR,file)
        if file.endswith(".pdf"):
            loader = PyPDFLoader(path)
        elif file.endswith(".txt"):
            loader = TextLoader(path)
        else:
            continue
        docs.extend(loader.load())
    return docs

def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=50)
    return splitter.split_documents(docs)

def build_faiss_index(docs):
    embeddings = LocalEmbeddingModel()
    return FAISS.from_documents(docs, embeddings)

def save_index(index):
    index.save_local(INDEX_DIR)

if __name__ == "__main__":
    print("📄 Loading medical documents...")
    docs = load_documents()
    print(f"✅ Loaded {len(docs)} documents.")

    print("🧩 Splitting into chunks...")
    chunks = split_documents(docs)
    print(f"✅ Created {len(chunks)} chunks.")

    print("📦 Creating FAISS index...")
    index = build_faiss_index(chunks)

    print("💾 Saving index...")
    save_index(index)

    print("✅ FAISS index built and saved successfully!")

    # Optional: test retrieval
    query = "What are symptoms of hypertension?"
    docs = index.similarity_search(query, k=3)
    for i, doc in enumerate(docs):
        print(f"\nResult {i+1}:\n{doc.page_content}")

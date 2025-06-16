import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import faiss
import pickle
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain.embeddings.base import Embeddings
from embeddings.local_embedding_model import LocalEmbeddingModel
from typing import List

class MemoryManager:
    def __init__(self, save_path: str = "day08_react_agent/faiss_index/"):
        self.save_path = save_path
        self.embedding_model: Embeddings = LocalEmbeddingModel()
        self.vectorstore = self._load_or_create_vectorstore()

    def _load_or_create_vectorstore(self):
        if os.path.exists(self.save_path):
            print("📂 Loading existing FAISS memory from disk...")
            return FAISS.load_local(
                self.save_path,
                self.embedding_model,
                allow_dangerous_deserialization=True  # ✅ added this line
            )

        print("🧠 Creating new FAISS memory store...")
        # Create dummy document to initialize
        dummy_docs = [Document(page_content="temporary init doc")]
        vectorstore = FAISS.from_documents(dummy_docs, self.embedding_model)
        dummy_id = list(vectorstore.docstore._dict.keys())[0]
        vectorstore.delete([dummy_id])
        return vectorstore

    def store_message(self, message: str, metadata: dict = {}):
        doc = Document(page_content=message, metadata=metadata)
        self.vectorstore.add_documents([doc])
        self.save_memory()

    def retrieve_relevant(self, query: str, k: int = 3):
        results = self.vectorstore.similarity_search(query, k=k)
        return results

    def save_memory(self):
        self.vectorstore.save_local(self.save_path)

    def get_all_memories(self) -> List[str]:
        if not self.index or not self.data:
            return []
        return [doc.page_content for doc in self.data]


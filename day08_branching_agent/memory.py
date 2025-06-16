import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import faiss
import pickle
from langchain_community.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.schema import Document
from embeddings.local_embedding_model import LocalEmbeddingModel


class MemoryManager:
    def __init__(self, index_path="faiss_index"):
        self.index_path = index_path
        self.embedder = LocalEmbeddingModel()
        self.vectorstore = self._load_or_create_vectortore()

    def _load_or_create_vectortore(self):
        if os.path.exists(f"{self.index_path}/faiss_store.pkl"):
            print(f"[Memory] Loading FAISS index from {self.index_path}...")
            with open(f"{self.index_path}/faiss_store.pkl", "rb") as f:
                return pickle.load(f)
        else:
            print("[Memory] Creating new FAISS index...")
            # Dynamically get embedding size
            dim = len(self.embedder.embed_query("sample"))
            index = faiss.IndexFlatL2(dim)
            return FAISS(
                embedding_function=self.embedder,
                index=index,
                docstore=InMemoryDocstore(),
                index_to_docstore_id={},
                normalize_L2=False,
            )

    def save(self):
        os.makedirs(self.index_path, exist_ok=True)
        with open(f"{self.index_path}/faiss_store.pkl", "wb") as f:
            pickle.dump(self.vectorstore, f)
        print("[Memory] Saved FAISS index to disk.")

    def add(self, text: str, metadata=None):
        doc = Document(page_content=text, metadata=metadata or {})
        self.vectorstore.add_documents([doc])
        self.save()

    def search(self, query: str, k: int = 5):
        return self.vectorstore.similarity_search(query, k=k)



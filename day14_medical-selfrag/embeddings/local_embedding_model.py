import logging
from typing import List, Any, Dict
from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings

# Set up logging
logger = logging.getLogger("LocalEmbeddingModel")
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
handler.setFormatter(formatter)
if not logger.hasHandlers():
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

class LocalEmbeddingModel(Embeddings):
    """
    Local embedding model wrapper using sentence-transformers.
    Compatible with LangChain vectorstores (FAISS, Chroma, etc).
    Supports batch embedding and single query embedding.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        self.model_name = model_name
        logger.info(f"Loading local model '{self.model_name}'...")
        self.model = SentenceTransformer(self.model_name)
        logger.info(f"Model '{self.model_name}' loaded successfully.")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        logger.info(f"Embedding {len(texts)} documents locally with model '{self.model_name}'...")
        embeddings = self.model.encode(texts, convert_to_numpy=True).tolist()
        logger.info(f"Successfully embedded {len(embeddings)} documents.")
        return embeddings

    def embed_query(self, text: str) -> List[float]:
        logger.info(f"Embedding query locally with model '{self.model_name}'...")
        embedding = self.model.encode(text, convert_to_numpy=True).tolist()
        logger.info("Successfully embedded query.")
        return embedding

    @property
    def config(self) -> Dict[str, Any]:
        return {"model_name": self.model_name}
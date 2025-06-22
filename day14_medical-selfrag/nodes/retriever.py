from state.selfrag_state import SelfRAGState
from langchain_community.vectorstores import FAISS
from embeddings.local_embedding_model import LocalEmbeddingModel
import os

FAISS_INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "vectorstore", "faiss_index")

def retriever_node(state:SelfRAGState) -> SelfRAGState:
    query = state.question
    logs = state.logs

    embeddings = LocalEmbeddingModel()
    db = FAISS.load_local(FAISS_INDEX_PATH,embeddings,allow_dangerous_deserialization=True)

    docs = db.similarity_search(query,k=4)
    doc_texts = [doc.page_content for doc in docs]

    logs.append(f"Retrieved {len(doc_texts)} documents from FAISS.")

    return state.model_copy(update={
        "retrieved_docs":doc_texts,
        "logs":logs
    })
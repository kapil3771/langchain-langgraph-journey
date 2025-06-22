from state.selfrag_state import SelfRAGState
from embeddings.local_embedding_model import LocalEmbeddingModel
from langchain_community.vectorstores import FAISS
import os

INDEX_PATH = os.path.abspath("vectorstore/faiss_index")

vectorstore = FAISS.load_local(INDEX_PATH, LocalEmbeddingModel(), allow_dangerous_deserialization=True)

def rerun_retrieval(state: SelfRAGState) -> SelfRAGState:
    query = state.question
    logs = state.logs

    try:
        docs = vectorstore.similarity_search(query, k=4)
        text_chunks = [doc.page_content for doc in docs]
        logs.append(f"🔄 Reretrieved {len(text_chunks)} docs using corrected query.")
    except Exception as e:
        text_chunks = []
        logs.append(f"Retry retrieval failed: {str(e)}")

    return state.model_copy(update={
    "retrieved_docs": text_chunks,
    "logs": logs
    })
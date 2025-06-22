from state.selfrag_state import SelfRAGState

TRUSTED_SOURCES = [
    "cdc", "who", "nih", "ncbi", "pubmed", "mayo clinic", 
    "cleveland clinic", "uptodate", "webmd", "medlineplus"
]

def is_trustworthy(doc: str) -> bool:
    lowered = doc.lower()
    return any(keyword in lowered for keyword in TRUSTED_SOURCES)

def trustrag_node(state: SelfRAGState) -> SelfRAGState:
    all_docs = state.retrieved_docs
    logs = state.logs

    trusted = [doc for doc in all_docs if is_trustworthy(doc)]

    logs.append(f"TrustRAG filtered {len(trusted)} of {len(all_docs)} docs as high-trust.")

    return state.model_copy(update={
    "trusted_docs": trusted,
    "logs": logs
    })
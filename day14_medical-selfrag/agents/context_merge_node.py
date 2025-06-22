from state.selfrag_state import SelfRAGState

def context_merge_node(state: SelfRAGState) -> SelfRAGState:
    retrieved_docs = getattr(state, "retrieved_docs", [])
    logs = state.logs

    if not retrieved_docs:
        final_context = "No documents available for context."
        logs.append("No docs to merge.")
    else:
        final_context = "\n\n---\n\n".join(retrieved_docs)
        logs.append(f"Merged {len(retrieved_docs)} retrieved docs into final_context.")

    return state.model_copy(update={
    "final_context": final_context,
    "logs": logs
    })
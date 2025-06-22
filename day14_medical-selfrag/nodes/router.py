from state.selfrag_state import SelfRAGState

MAX_RETRIES = 3

def retry_router(state: SelfRAGState) -> str:
    grade = state.grade
    token = state.reflection_token
    retries = state.retry_count
    logs = state.logs.copy()

    if grade == "correct":
        logs.append("Answer is correct. Stopping execution.")
        return "answer_node"
    
    if retries >= MAX_RETRIES:
        logs.append("Max retries reached. Returning best effort answer.")
        return "answer_node"
    
    new_retry_count = retries + 1
    state = state.model_copy(update={"retry_count": new_retry_count, "logs": logs})
    
    if token == "ISREL":  # Retry with corrected query
        logs.append("Rerouting to corrected retrieval based on ISREL token.")
        return "rerun_retrieval"
    elif token == "ISSUP":  # Use same docs, try again
        logs.append("Reusing current docs. Rerouting to context merge.")
        return "context_merge"
    elif token == "ISUSE":  # Skip correction, just answer anyway
        logs.append("Forcing answer despite low grade (ISUSE).")
        return "answer_node"
    elif token == "ISREL_HALLUCINATED":
        logs.append("Rerouting due to major hallucination.")
        return "rerun_retrieval"
    else:
        logs.append("Unknown token, defaulting to rerun_retrieval.")
        return "rerun_retrieval"

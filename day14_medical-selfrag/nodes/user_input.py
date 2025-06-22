from state.selfrag_state import SelfRAGState

def user_input_node(state: SelfRAGState) -> SelfRAGState:
    question = getattr(state, "question", "What is hypertension?")
    return state.model_copy(update={
        "question": question,
        "retrieved_docs": [],
        "trusted_docs": [],
        "corrected_docs": None,
        "correction_reason": None,
        "hallucination_spans": [],
        "grade": "incorrect",
        "feedback": "",
        "reflection_token": "ISREL",
        "final_context": "",
        "answer": "",
        "logs": [f"Received user query: {question}"],
        "retry_count": 0,
        "messages": [],
    })
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.corrector_node import corrector_node
from state.selfrag_state import SelfRAGState
from pprint import pprint

state: SelfRAGState = {
    "question": "Blood heart stroke pipe?",
    "retrieved_docs": ["Some random unrelated text.", "Nothing useful found."],
    "grade": "incorrect",
    "feedback": "The documents are vague and unrelated to the query.",
    "correction_reason": None,
    "corrected_docs": None,
    "final_context": "",
    "answer": "",
    "logs": ["🚫 Grader flagged poor retrieval."],
    "messages": [],
    "reflection_token": "ISREL",
    "retry_count": 1,
    "trusted_docs": [],
    "hallucination_spans": []
}

if __name__ == "__main__":
    print("🛠️ Testing corrector_node...\n")
    updated = corrector_node(state)
    pprint({
        "corrected_query": updated["question"],
        "correction_reason": updated["correction_reason"],
        "logs": updated["logs"][-2:]
    })
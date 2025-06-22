import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from nodes.rerun_retrieval import rerun_retrieval
from state.selfrag_state import SelfRAGState
from pprint import pprint

state: SelfRAGState = {
    "question": "What causes hypertension?",
    "retrieved_docs": [],
    "logs": ["🛠️ Corrected query applied."],
    "grade": "incorrect",
    "feedback": "",
    "correction_reason": "Previous docs lacked biological explanations",
    "corrected_docs": None,
    "final_context": "",
    "answer": "",
    "messages": [],
    "reflection_token": "ISREL",
    "retry_count": 1,
    "trusted_docs": [],
    "hallucination_spans": []
}

if __name__ == "__main__":
    print("🔁 Testing rerun_retrieval...\n")
    updated = rerun_retrieval(state)
    pprint({
        "retrieved_docs (snippet)": updated["retrieved_docs"][:2],
        "log": updated["logs"][-1]
    })
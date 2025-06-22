import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.context_merge_node import context_merge_node
from state.selfrag_state import SelfRAGState
from pprint import pprint

state: SelfRAGState = {
    "question": "What causes hypertension?",
    "retrieved_docs": [
        "Hypertension is caused by a variety of genetic and lifestyle factors...",
        "Key factors include high sodium intake, stress, and lack of exercise..."
    ],
    "logs": ["🔁 Docs reretrieved."],
    "grade": "incorrect",
    "feedback": "",
    "correction_reason": "",
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
    updated = context_merge_node(state)
    print("\n📚 Merged Final Context:\n")
    print(updated["final_context"][:300] + "...")
    print("\n📝 Log:", updated["logs"][-1])
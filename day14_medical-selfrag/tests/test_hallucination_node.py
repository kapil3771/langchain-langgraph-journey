# File: tests/test_hallucination_node.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.hallucination_node import hallucination_node
from state.selfrag_state import SelfRAGState
from pprint import pprint

state: SelfRAGState = {
    "question": "What is hypertension?",
    "answer": "Hypertension is caused by alien parasites that alter blood flow.",
    "final_context": "Hypertension is commonly caused by kidney disease, hormonal imbalance, or lifestyle factors like poor diet and stress.",
    "logs": [],
    "retrieved_docs": [],
    "grade": "correct",
    "feedback": "",
    "correction_reason": "",
    "corrected_docs": None,
    "messages": [],
    "retry_count": 1,
    "reflection_token": "ISREL",
    "trusted_docs": [],
    "hallucination_spans": []
}

if __name__ == "__main__":
    result = hallucination_node(state)
    pprint(result["hallucination_spans"])
    print("🪵 Log:", result["logs"][-1])
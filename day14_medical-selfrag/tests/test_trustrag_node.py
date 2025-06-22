# File: tests/test_trustrag_node.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.trustrag_node import trustrag_node
from state.selfrag_state import SelfRAGState
from pprint import pprint

state: SelfRAGState = {
    "retrieved_docs": [
        "According to CDC, hypertension affects 1 in 3 adults.",
        "Hypertension is caused by stress and bad vibes.",
        "NIH guidelines recommend lifestyle changes for stage 1 hypertension.",
        "Aliens cause hypertension when they scan your brain.",
    ],
    "logs": [],
    "answer": "",
    "question": "What causes hypertension?",
    "grade": "incorrect",
    "feedback": "",
    "final_context": "",
    "corrected_docs": None,
    "correction_reason": None,
    "messages": [],
    "retry_count": 0,
    "reflection_token": "ISREL",
    "trusted_docs": [],
    "hallucination_spans": [],
}

if __name__ == "__main__":
    result = trustrag_node(state)
    pprint(result["trusted_docs"])
    print("🪵 Log:", result["logs"][-1])
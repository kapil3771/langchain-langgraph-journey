# File: tests/test_answer_node.py

import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.answer_node import answer_node
from state.selfrag_state import SelfRAGState
from pprint import pprint

state = SelfRAGState(
    question="What is hypertension?",
    final_context=(
        "Hypertension, also known as high blood pressure, is a condition where the force of the blood "
        "against the artery walls is too high. It is commonly defined as having a blood pressure reading "
        "consistently at or above 130/80 mmHg."
    ),
    logs=["📚 Final context merged."],
    retrieved_docs=[],
    grade="correct",
    feedback="",
    correction_reason=None,
    corrected_docs=None,
    answer="",
    messages=[],
    reflection_token="ISREL",
    retry_count=1,
    trusted_docs=[],
    hallucination_spans=[]
)

if __name__ == "__main__":
    updated = answer_node(state)
    print("\n💬 Final Answer:\n")
    print(updated.answer)  # ✅ Use dot access instead of updated["answer"]

    print("\n📝 Log:", updated.logs[-1])
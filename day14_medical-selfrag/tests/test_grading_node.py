import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.grading_node import grading_node
from state.selfrag_state import SelfRAGState
from pprint import pprint

# 🧪 Simulate input after retriever_node
state: SelfRAGState = {
    "question": "What is hypertension?",
    "retrieved_docs": [
        "Hypertension, or high blood pressure, is when the force of blood against artery walls is too high. It can lead to heart disease, stroke, and kidney failure.",
        "Primary hypertension has no clear cause and develops over time, while secondary hypertension is caused by other conditions like kidney disease.",
        "Symptoms are often silent, but severe hypertension may cause headaches, vision problems, or chest pain.",
        "Blood pressure is measured in mmHg, and a reading consistently above 130/80 mmHg is considered hypertensive."
    ],
    "grade": "incorrect",  # will be updated
    "feedback": "",
    "correction_reason": None,
    "corrected_docs": None,
    "final_context": "",
    "answer": "",
    "logs": ["🧪 Simulated retriever output for hypertension."],
    "messages": [],
    "reflection_token": "ISREL",
    "retry_count": 0,
    "trusted_docs": [],
    "hallucination_spans": []
}

if __name__ == "__main__":
    print("🔍 Testing grading_node...\n")
    updated_state = grading_node(state)
    pprint({
        "grade": updated_state["grade"],
        "feedback": updated_state["feedback"],
        "reflection_token": updated_state["reflection_token"],
        "logs": updated_state["logs"][-3:],  # Last 3 logs
    })
from typing import Literal
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from state.selfrag_state import SelfRAGState
import json

llm = ChatOllama(model="gemma:2b", temperature=0.3)

def grading_node(state: SelfRAGState) -> SelfRAGState:
    question = state.question
    docs = state.retrieved_docs
    logs = state.logs.copy()  # Create a copy to avoid mutation issues

    prompt = f"""
You are a retrieval quality evaluator in a Self-RAG system.

Given the user query and the retrieved context, grade the usefulness of the context.

User Question:
{question}

Retrieved Docs:
{chr(10).join(docs)}

---

Respond in JSON format:
{{
    "grade": "correct|incorrect|ambiguous",
    "feedback": "one-line reason",
    "reflection_token": "ISREL|ISUSE|ISSUP"
}}
"""
    
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        parsed = json.loads(response.content)
        grade = parsed.get("grade", "incorrect").strip().lower()
        feedback = parsed.get("feedback", "No feedback.").strip()
        reflection = parsed.get("reflection_token", "ISREL").strip()
    except Exception as e:
        grade = "incorrect"
        feedback = f"Failed to parse JSON grading response: {str(e)}"
        reflection = "ISREL"
    
    logs.append(f"Grading: {grade.upper()} — {feedback}")
    logs.append(f"Reflection Token → {reflection}")

    return state.model_copy(update={
        "grade": grade,
        "feedback": feedback,
        "reflection_token": reflection,
        "logs": logs
    })
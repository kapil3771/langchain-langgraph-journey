from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from state.selfrag_state import SelfRAGState
import json

llm = ChatOllama(model="gemma:2b", temperature=0.3)

def corrector_node(state: SelfRAGState) -> SelfRAGState:
    question = state.question
    docs = state.retrieved_docs
    feedback = state.feedback
    logs = state.logs

    prompt = f"""
You're an expert query correction agent in a medical QA system.

The system failed to retrieve useful documents for the question below.

Question:
{question}

Retrieved Docs:
{chr(10).join(docs)}

Grader Feedback:
{feedback}

---

Please rewrite the search query to improve retrieval quality.
Respond ONLY in this JSON format:
{{
  "correction_reason": "...",
  "corrected_query": "..."
}}
"""

    try:
        response = llm.invoke([HumanMessage(content=prompt)]).content
        parsed = json.loads(response)

        corrected_query = parsed.get("corrected_query", question).strip()
        correction_reason = parsed.get("correction_reason", "Unknown reason").strip()

    except Exception as e:
        corrected_query = question
        correction_reason = f"Failed to parse correction: {str(e)}"

    logs.append(f"Query rewritten: {corrected_query}")
    logs.append(f"Reason: {correction_reason}")

    return state.model_copy(update={
    "question": corrected_query,
    "correction_reason": correction_reason,
    "logs": logs
    })
from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from state.selfrag_state import SelfRAGState
import json

llm = ChatOllama(model="gemma:2b", temperature=0.3)

def hallucination_node(state: SelfRAGState) -> SelfRAGState:
    answer = state.answer
    context = state.final_context
    logs = state.logs.copy()

    prompt = f"""
You are a hallucination detector for a medical QA system.

Here is the final generated answer:
{answer}

And here is the context the answer was based on:
{context}

Identify if any parts of the answer are **not grounded** in the context.
Return a JSON list of hallucinated spans (copy-pasted from the answer) that are not entailed by the context.

Respond only in this JSON format:
{{"hallucinations": ["...span1...", "...span2..."]}}
"""

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        parsed = json.loads(response.content)
        hallucinated = parsed.get("hallucinations", [])
    except Exception:
        hallucinated = ["[Error parsing hallucination check]"]

    hallucination_count = len(hallucinated)
    logs.append(f"Hallucination spans detected: {hallucinated if hallucinated else 'None'}")

    # State-Aware Hallucination Handling
    if hallucinated and "Error" not in str(hallucinated[0]):
        if hallucination_count > 2:
            logs.append("Major hallucination detected. Triggering retry loop.")
            reflection_token = "ISREL_HALLUCINATED"
            grade = "incorrect"
        else:
            logs.append("Minor hallucinations found. Proceeding without retry.")
            reflection_token = state.reflection_token
            grade = state.grade
    else:
        logs.append("No hallucinations. Finalizing answer.")
        reflection_token = state.reflection_token
        grade = state.grade

    return state.model_copy(update={
        "hallucination_spans": hallucinated,
        "reflection_token": reflection_token,
        "grade": grade,
        "logs": logs
    })
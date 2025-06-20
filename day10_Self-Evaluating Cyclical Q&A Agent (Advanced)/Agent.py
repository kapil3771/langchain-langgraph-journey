from typing import TypedDict, Optional, List
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.graph.schema import entrypoint, task # type: ignore
from langchain_ollama import ChatOllama
import os

llm = ChatOllama(model="openchat", temperature=0.2)

class EvalState(TypedDict):
    question: str
    answer: Optional[str]
    score: Optional[float]
    retries: int
    logs: List[str]
    debug: bool 

@entrypoint
def start(state: EvalState) -> EvalState:
    if state["debug"]:
        state["logs"].append("Starting question answering...")
    return state

@task
def answer(state: EvalState) -> EvalState:
    prompt = f"Q: {state['question']}\nA:"
    answer = llm.invoke(prompt).content
    if state["debug"]:
        state["logs"].append(f"Generated Answer: {answer}")
    return {**state, "answer": answer}

@task
def grade(state: EvalState) -> EvalState:
    grading_prompt = (
        f"You are a strict answer grader.\n"
        f"Question: {state['question']}\n"
        f"Answer: {state['answer']}\n"
        f"Give a score from 0.0 (wrong) to 1.0 (perfect). Only return the number."
    )
    try:
        score_raw = llm.invoke(grading_prompt).content.strip()
        score = float(score_raw)
    except Exception:
        score = 0.0

    retries = state["retries"] + 1
    if state["debug"]:
        state["logs"].append(f"Grading result: {score} (Retry {retries})")
    return {**state, "score": score, "retries": retries}

def router(state: EvalState) -> str:
    if state["score"] and state["score"] >= 0.8:
        if state["debug"]:
            state["logs"].append("Score high enough, finishing.")
        return "end"
    elif state["retries"] < 3:
        if state["debug"]:
            state["logs"].append("Retrying due to low score.")
        return "answer"
    else:
        return "fallback"

@task
def fallback(state: EvalState) -> EvalState:
    msg = "⚠️ Sorry, I couldn't answer confidently."
    if state["debug"]:
        state["logs"].append("Reached fallback after 3 retries.")
    return {**state, "answer": msg}

builder = StateGraph(EvalState)
builder.add_node("start", start)
builder.add_node("answer", answer)
builder.add_node("grade", grade)
builder.add_node("fallback", fallback)

builder.set_entry_point("start")
builder.add_edge("start", "answer")
builder.add_edge("answer", "grade")
builder.add_conditional_edges("grade", router, {
    "answer": "answer",
    "fallback": "fallback",
    "end": END,
})

graph = builder.compile()
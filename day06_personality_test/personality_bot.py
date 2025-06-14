from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal
from langchain_core.runnables import RunnableLambda


class PersonalityState(TypedDict):
    answers: list[str]
    result: str


def ask_q1(state: PersonalityState) -> PersonalityState:
    print("Q1: Do you enjoy large social gatherings? (yes/no)")
    answer = input("You: ").strip().lower()
    return {"answers": state["answers"] + [answer]}

def ask_q2(state: PersonalityState) -> PersonalityState:
    print("Q2: Do you often need alone time to recharge? (yes/no)")
    answer = input("You: ").strip().lower()
    return {"answers": state["answers"] + [answer]}

def ask_q3(state: PersonalityState) -> PersonalityState:
    print("Q3: Do you feel comfortable in both social and quiet settings? (yes/no)")
    answer = input("You: ").strip().lower()
    return {"answers": state["answers"] + [answer]}

def evaluate(state: PersonalityState) -> PersonalityState:
    answers = state["answers"]
    yes_count = answers.count("yes")
    no_count = answers.count("no")

    if yes_count >= 2:
        result = "Extrovert"
    elif no_count >= 2:
        result = "Introvert"
    else:
        result = "Ambivert"

    print(f"🧠 Personality Type: {result}")
    return {"answers": answers, "result": result}


builder = StateGraph(PersonalityState)

builder.add_node("q1", RunnableLambda(ask_q1))
builder.add_node("q2", RunnableLambda(ask_q2))
builder.add_node("q3", RunnableLambda(ask_q3))
builder.add_node("evaluate", RunnableLambda(evaluate))

builder.set_entry_point("q1")
builder.add_edge("q1", "q2")
builder.add_edge("q2", "q3")
builder.add_edge("q3", "evaluate")
builder.set_finish_point("evaluate")


app = builder.compile()
app.invoke({"answers": []})
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal, Optional

from day08_branching_agent.intent_classifier import classify_intent
from day08_branching_agent.memory import MemoryManager
from day08_branching_agent.branching_agent import handle_chitchat, handle_task


from datetime import datetime

memory = MemoryManager()

class AgentState(TypedDict):
    input : str
    intent: Optional[Literal["chitchat", "task"]]
    response: Optional[str]

def route_intent(state: AgentState) -> AgentState:
    intent = classify_intent(state["input"])
    return {**state, "intent": intent}

def chitchat_node(state: AgentState) -> AgentState:
    response = handle_chitchat(state["input"])
    return {**state, "response": response}

def task_node(state: AgentState) -> AgentState:
    response = handle_task(state["input"])
    return {**state, "response": response}

def save_to_memory(state: AgentState) -> AgentState:
    memory.add(f"User: {state['input']}\nAgent: {state['response']}", metadata={"intent": state["intent"]})
    return state

def get_agent_graph():
    builder = StateGraph(AgentState)

    builder.add_node("classify", route_intent)
    builder.add_node("chitchat", chitchat_node)
    builder.add_node("task", task_node)
    builder.add_node("save", save_to_memory)

    builder.set_entry_point("classify")

    builder.add_conditional_edges(
        "classify",
        lambda state: state["intent"],
        {
            "chitchat": "chitchat",
            "task": "task",
        }
    )

    builder.add_edge("chitchat", "save")
    builder.add_edge("task", "save")
    builder.add_edge("save", END)

    return builder.compile()

if __name__ == "__main__":
    graph = get_agent_graph()
    user_input = input("You: ")
    final_state = graph.invoke({"input": user_input})
    print(f"\n[Intent: {final_state['intent']}]")
    print(f"Agent: {final_state['response']}")
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Classic LangGraph API - Compatible with older versions
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import TypedDict, Literal, Annotated, List
from langchain_core.messages import AIMessage, HumanMessage
from langchain_ollama import ChatOllama

class State(TypedDict):
    messages: Annotated[List, lambda x, y: x + y]
    retry_count: int
    logs: List[str]
    grade: Literal["correct", "incorrect", "ambiguous"]

llm = ChatOllama(model="gemma:2b", temperature=0.3)

def start_node(state: State) -> State:
    return {
        "messages": [HumanMessage(content="What is the capital of France?")],
        "retry_count": 0,
        "logs": ["Start node triggered"],
        "grade": "incorrect"
    }

def chatbot_node(state: State) -> State:
    messages = state["messages"]
    logs = state["logs"].copy()

    response = llm.invoke(messages)
    logs.append("LLM response generated")

    return {
        "messages": messages + [response],
        "logs": logs,
        "retry_count": state["retry_count"] + 1,
        "grade": "incorrect"
    }

def grader_node(state: State) -> State:
    messages = state["messages"]
    logs = state["logs"].copy()

    answer = messages[-1].content.lower() if messages else ""

    if "paris" in answer:
        grade = "correct"
    elif len(answer.strip()) < 20:
        grade = "incorrect"
    else:
        grade = "ambiguous"
    
    logs.append(f"Grader judged answer as {grade}")

    return {
        "messages": messages,
        "retry_count": state["retry_count"],
        "logs": logs,
        "grade": grade
    }

def grade_router(state: State) -> str:
    """Route based on grade and retry count"""
    if state["grade"] == "correct":
        return "end"
    elif state["retry_count"] >= 5:
        return "end"
    else:
        return "chatbot"

# Build the graph using StateGraph
workflow = StateGraph(State)

# Add nodes
workflow.add_node("start", start_node)
workflow.add_node("chatbot", chatbot_node)
workflow.add_node("grader", grader_node)

# Add edges
workflow.add_edge("start", "chatbot")
workflow.add_edge("chatbot", "grader")
workflow.add_conditional_edges(
    "grader",
    grade_router,
    {
        "chatbot": "chatbot",
        "end": END
    }
)

# Set entry point
workflow.set_entry_point("start")

# Compile the graph
graph = workflow.compile(checkpointer=MemorySaver())

if __name__ == "__main__":
    thread_id = "cap_fr"
    config = {"configurable": {"thread_id": thread_id}}

    print("🚀 Starting France Capital Quiz...")
    
    for step in graph.stream({}, config, stream_mode="values"):
        if "logs" in step:
            print("\n--- Step ---")
            for log in step["logs"]:
                print(f"📝 {log}")
        
        # Print current state info
        if "retry_count" in step and step["retry_count"] > 0:
            print(f"🔄 Retry count: {step['retry_count']}")
        if "grade" in step:
            print(f"📊 Grade: {step['grade']}")
            
        if step.get("grade") == "correct":
            print("\n✅ Correct Answer Found!")
            print("🎯 Final Answer:", step["messages"][-1].content)
            break
        elif step.get("retry_count", 0) >= 5:
            print("\n❌ Max retries reached!")
            if step.get("messages"):
                print("🔴 Last answer:", step["messages"][-1].content)
            break

    print("\n🏁 Quiz completed!")
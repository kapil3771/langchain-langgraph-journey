import math, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import TypedDict, Optional, Annotated, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_ollama import ChatOllama
import wikipedia

class AgentState(TypedDict):
    question: str
    wikipedia_answer: Optional[str]
    calculator_answer: Optional[str]
    final_response: Optional[str]
    messages: List[BaseMessage]

llm = ChatOllama(model="gemma:2b", temperature=0.3)

def research_agent(state: AgentState) -> AgentState:
    try:
        summary = wikipedia.summary(state["question"], sentences=2)
    except:
        summary = "No Wikipedia data found."
    return {**state, "wikipedia_answer": summary}

SAFE_MATH_FUNCS = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
SAFE_MATH_FUNCS.update({"abs": abs, "round": round})

def calculator_agent(state: AgentState) -> AgentState:
    try:
        calc_input = state["question"]
        result = eval(calc_input, {"__builtins__": {}}, SAFE_MATH_FUNCS)
        output = f"🧮 {calc_input} = {result}"
    except Exception as e:
        output = f"❌ Calculator Error: {str(e)}"
    return {**state, "calculator_answer": output}

def supervisor_node(state: AgentState) -> AgentState:
    return state

def route_decision(state: AgentState) -> str:
    q = state["question"].lower()
    if any(x in q for x in ["population", "country", "city", "who", "what", "when"]):
        return "research_agent"
    elif any(x in q for x in ["sqrt", "*", "/", "+", "-", "^", "calc", "evaluate"]):
        return "calculator_agent"
    return "finalizer"

def final_node(state: AgentState) -> AgentState:
    context = []
    if state.get("wikipedia_answer"):
        context.append("Wikipedia: " + state["wikipedia_answer"])
    if state.get("calculator_answer"):
        context.append("Calc: " + state["calculator_answer"])

    prompt = f"""User Question: {state['question']}
Relevant Info:\n{chr(10).join(context)}

Answer the user question as best as possible."""
    answer = llm.invoke([HumanMessage(content=prompt)]).content
    return {**state, "final_response": answer}

workflow = StateGraph(AgentState)
workflow.add_node("supervisor", supervisor_node)
workflow.add_node("research_agent", research_agent)
workflow.add_node("calculator_agent", calculator_agent)
workflow.add_node("finalizer", final_node)

workflow.set_entry_point("supervisor")
workflow.add_conditional_edges("supervisor", route_decision, {
    "research_agent": "research_agent",
    "calculator_agent": "calculator_agent",
    "finalizer": "finalizer"
})

workflow.add_edge("research_agent", "finalizer")
workflow.add_edge("calculator_agent", "finalizer")
workflow.set_finish_point("finalizer")

graph = workflow.compile()

if __name__ == "__main__":
    question = input("Ask something: ")
    result = graph.invoke({"question": question, "messages": []})
    print("\n🧠 Final Answer:")
    print(result["final_response"])
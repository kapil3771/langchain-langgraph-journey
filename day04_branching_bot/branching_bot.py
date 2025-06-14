from langgraph.graph import StateGraph
from typing import TypedDict, Literal
from langchain_core.runnables import RunnableLambda

class SupportState(TypedDict):
    user_input: str
    response: str

def start(state: SupportState) ->SupportState:
    print("🤖 Bot: Hi! How can I help you today?")
    user_input = input("👤 You: ")
    return {
        "user_input":user_input
    }

def route_decision(state:SupportState) -> SupportState:
    return state

def billing_support(state:SupportState) ->SupportState:
    print("💳 Billing: I can help you with billing issues.")
    return{
        "response": "billing help provided"
    }

def tech_support(state:SupportState) ->SupportState:
    print("🛠️ Tech Support: Let's fix your technical issue.")
    return{
        "response": "tech help provided"
    }

def fallback(state:SupportState) ->SupportState:
    print("🤷 Sorry, I didn't understand. Can you rephrase?")
    return {
        "response": "fallback triggered"
    }

def route(state: SupportState) -> Literal["billing", "tech", "unknown"]:
    user_input = state["user_input"].lower()
    if "billing" in user_input or "payment" in user_input:
        return "billing"
    elif "technical" in user_input or "tech" in user_input:
        return "tech"
    else:
        return "unknown"
    
builder = StateGraph(SupportState)

builder.add_node("start", RunnableLambda(start))
builder.add_node("route_decision", RunnableLambda(route_decision))
builder.add_node("billing", RunnableLambda(billing_support))
builder.add_node("tech", RunnableLambda(tech_support))
builder.add_node("fallback", RunnableLambda(fallback))

builder.set_entry_point("start")
builder.set_finish_point("billing")
builder.set_finish_point("tech")
builder.set_finish_point("fallback")

builder.add_edge("start","route_decision")

builder.add_conditional_edges(
    "route_decision",
    route,
    {
        "billing":"billing",
        "tech":"tech",
        "unknown":"fallback"
    }
)

app = builder.compile()
app.invoke({})
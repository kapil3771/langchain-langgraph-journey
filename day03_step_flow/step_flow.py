from langgraph.graph import StateGraph,END
from typing import TypedDict

class StepState(TypedDict):
    name : str
    greeting: str
    question: str
    answer: str

def greet(state:StepState)-> StepState:
    name = state["name"]
    return{
        **state,
        "greeting": f"Hello, {name}!"
    }

def ask_followup(state:StepState)-> StepState:
    follow_q = f"{state['name']}, what would you like to learn?"
    return{
        **state,
        "question":follow_q
    }

def final_response(state:StepState) -> StepState:
    resp = (
        f"{state['greeting']}\n"
        f"{state['question']}\n"
        f"(This concludes our 3‑step assistant demo.)"
    )
    return {
        **state,
        "answer":resp
    }

def farewell(state:StepState) -> StepState:
    return {
        **state,
        "answer": state["answer"] + "\nSee you soon!"
    }


graph = StateGraph(StepState)

graph.add_node("greet", greet)
graph.add_node("ask", ask_followup)
graph.add_node("respond", final_response)
graph.add_node("farewell", farewell)

graph.add_edge("greet","ask")
graph.add_edge("ask","respond")
graph.add_edge("respond","farewell")

graph.set_entry_point("greet")
graph.set_finish_point("farewell")

assistant_flow = graph.compile()

if __name__ == "__main__":
    result = assistant_flow.invoke({"name":"kapil"})
    print(result["answer"])
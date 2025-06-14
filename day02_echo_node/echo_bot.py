from langgraph.graph import StateGraph, END
from typing import TypedDict

class EchoState(TypedDict):
    input: str
    output: str

def echo_node(state: EchoState) -> EchoState:
    user_input = state['input']
    return {
        "input":user_input,
        "output": f"Echo: {user_input}"
    }

graph = StateGraph(EchoState)
graph.add_node("echo",echo_node)
graph.set_entry_point("echo")
graph.set_finish_point("echo")

echo_chain = graph.compile()

result = echo_chain.invoke({"input":"hello kapil"})
print(result)
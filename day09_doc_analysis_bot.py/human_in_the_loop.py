import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from typing import Annotated
from typing_extensions import TypedDict

from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import Command, interrupt
from langchain_ollama import ChatOllama

os.environ["TAVILY_API_KEY"] = "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"

llm = ChatOllama(
    model="gemma:2b",
    temperature=0.3,
)
llm_with_tools = None  

class State(TypedDict):
    messages: Annotated[list, add_messages]  

@tool
def human_assistance(query: str) -> str:
    """Request assistance from a human (interrupt execution)."""
    human_response = interrupt({"query": query}) 
    return human_response["data"] 

search_tool = TavilySearch(max_results=2)
tools = [search_tool, human_assistance]
llm_with_tools = llm.bind_tools(tools) 

def chatbot_node(state: State) -> State:
    message = llm_with_tools.invoke(state["messages"])
    return {"messages": [message]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot_node)
graph_builder.add_node("tools", ToolNode(tools=tools))

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition, 
)

graph_builder.add_edge("tools", "chatbot")

graph_builder.add_edge(START, "chatbot")


memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "1"}}

    user_input = "I need help building an AI agent, please ask a human."
    events = graph.stream({"messages": user_input}, config, stream_mode="values")

    for event in events:
        if "messages" in event:
            print("\n--- Chatbot Output ---")
            print(event["messages"][-1].content)

    human_response = (
        "Yes! We recommend using LangGraph. It is robust and powerful for agents."
    )
    command = Command(resume={"data": human_response})

    resumed = graph.stream(command, config, stream_mode="values")
    for event in resumed:
        if "messages" in event:
            print("\n--- Final Answer ---")
            print(event["messages"][-1].content)
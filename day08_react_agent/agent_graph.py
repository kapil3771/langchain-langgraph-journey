# day08_react_agent/agent_graph.py

from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
from langchain_core.runnables import RunnableConfig
from typing import TypedDict, List
import re

from local_llm import LocalLLM
from tools import tool_router
from memory import MemoryManager

# Initialize components
llm = LocalLLM()
memory = MemoryManager()

# Stronger SYSTEM_PROMPT to enforce correct tool usage
SYSTEM_PROMPT = """You are a helpful AI agent that uses tools when needed.

📌 Tool Use Format:
To use a tool, your response MUST follow this exact format (nothing else):
Action: tool_name[query]

✅ Valid tools:
- calculator
- wikipedia
- file_search

🔍 Examples (MUST follow exactly):
- Action: calculator[3 * (2 + 1)]
- Action: wikipedia[Python programming language]
- Action: file_search[deep learning]

🚫 NEVER say:
- 'Tool: ...'
- 'use tool ...'
- 'search on wikipedia ...'
- or explain the tool call

Just reply ONLY with the exact Action: line. If no tool is needed, respond normally.

✳️ Say this to yourself before responding:
“I will ONLY use tool_name[query] in 'Action:' format — NO deviations!”
"""

# Agent state
class AgentState(TypedDict):
    messages: List[BaseMessage]

# Plan Node — decide what to do
def plan_node(state: AgentState) -> AgentState:
    messages = state["messages"]
    user_input = messages[-1].content.strip()

    # Direct calculator override
    if user_input.lower().startswith("calculate:"):
        calc_expr = user_input.split(":", 1)[1].strip()
        response = f"Action: calculator[{calc_expr}]"
        messages.append(AIMessage(content=response))
        return {"messages": messages}

    # Memory retrieval
    context_docs = memory.retrieve_relevant(user_input)
    context_text = "\n".join([doc.page_content for doc in context_docs])

    system_msg = HumanMessage(content=SYSTEM_PROMPT)
    if context_text.strip():
        memory_msg = HumanMessage(content=f"📌 Memory (for context only, do NOT copy this):\n{context_text}")
        messages = [system_msg, memory_msg] + messages
    else:
        messages = [system_msg] + messages

    # LLM output
    response = llm.run(messages).strip()
    messages.append(AIMessage(content=response))
    return {"messages": messages}

# Tool Executor Node
def tool_executor_node(state: AgentState) -> AgentState:
    last_message = state["messages"][-1]
    tool_name, query = None, None

    match = re.match(r"Action:\s*([a-zA-Z_]+)\s*\[(.+?)\]\s*$", last_message.content.strip(), re.IGNORECASE)
    if match:
        tool_name = match.group(1).lower()
        query = match.group(2).strip()
    else:
        tool_response = "❌ Failed to parse tool call: use format → Action: tool[query]"
        return {"messages": state["messages"] + [AIMessage(content=tool_response)]}

    # ✅ Tool validation
    valid_tools = {"calculator", "wikipedia", "file_search"}
    if tool_name not in valid_tools:
        tool_response = f"❌ Unknown tool requested: '{tool_name}'. Valid tools: {', '.join(valid_tools)}"
        return {"messages": state["messages"] + [AIMessage(content=tool_response)]}

    try:
        tool_response = tool_router(tool_name, query)
    except Exception as e:
        tool_response = f"❌ Tool error: {str(e)}"

    return {"messages": state["messages"] + [AIMessage(content=f"✅ Result: {tool_response}")]}

# Edge logic — check if tool was requested
def needs_tool(state: AgentState) -> str:
    last_msg = state["messages"][-1]
    if isinstance(last_msg, AIMessage) and "Action:" in last_msg.content:
        return "tools"
    else:
        return "end"

# Final Node — persist to memory
def final_node(state: AgentState) -> AgentState:
    for msg in state["messages"]:
        if isinstance(msg, (HumanMessage, AIMessage)):
            memory.store_message(msg.content)
    return state

# Build LangGraph
workflow = StateGraph(AgentState)
workflow.add_node("plan", plan_node)
workflow.add_node("tool_executor", tool_executor_node)
workflow.add_node("final", final_node)

workflow.set_entry_point("plan")
workflow.add_conditional_edges("plan", needs_tool, {
    "tools": "tool_executor",
    "end": "final"
})
workflow.add_edge("tool_executor", "final")
workflow.set_finish_point("final")

graph = workflow.compile()

# Wrapper for UI
def run_agent(user_input: str, memory: MemoryManager):
    inputs = {"messages": [HumanMessage(content=user_input)]}
    result = graph.invoke(inputs, config=RunnableConfig())
    messages = result["messages"]

    final_reply = next((m.content for m in reversed(messages) if isinstance(m, AIMessage)), "")

    tools_used = []
    for m in messages:
        if isinstance(m, AIMessage):
            content = m.content.strip().lower()
            if any(x in content for x in [
                "✅ result:", "📚 wikipedia summary", "✅ found in",
                "🔍 no relevant files", "❌ tool error", "❌ calculator error",
                "❌ wikipedia error"
            ]):
                tools_used.append(m.content)

    return final_reply, tools_used
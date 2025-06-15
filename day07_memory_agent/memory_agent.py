import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import List, TypedDict
from langgraph.graph import StateGraph, END
from langchain_community.vectorstores import FAISS
from langchain_community.chat_models import ChatOllama
from embeddings.local_embedding_model import LocalEmbeddingModel


# --------- Memory State Definition ---------
class MemoryState(TypedDict):
    messages: List[str]


# --------- Setup Embedding + LLM + VectorStore ---------
embedder = LocalEmbeddingModel()  # Your local embedding model
llm = ChatOllama(model="gemma:2b")  # Your local LLM
vectorstore = FAISS.from_texts(["User asked about pricing"], embedder)  # Dummy init


# --------- Start Conversation ---------
def start_conversation(state: MemoryState) -> MemoryState:
    print("🤖 Bot: Chat:.")
    user_input = input("👤 You: ").strip()

    messages = state.get("messages", [])
    messages.append(f"User: {user_input}")

    return {
        "messages": messages,
        "next": "respond" if user_input.lower() not in ["bye", "exit", "quit"] else "end"
    }


# --------- Retrieve Relevant Memory & Respond ---------
def retrieve_and_respond(state: MemoryState) -> MemoryState:
    messages = state["messages"]
    latest_user_input = messages[-1].replace("User: ", "")

    # Only add past user+bot messages (excluding the latest input)
    vectorstore.add_texts(messages[:-1])

    retrieved_docs = vectorstore.similarity_search(latest_user_input, k=3)
    context = "\n".join([doc.page_content for doc in retrieved_docs])

    prompt = f"""You are a helpful, kind, emotionally aware AI assistant.
    
Here is past conversation memory:
{context}

User just said:
{latest_user_input}

Respond empathetically:"""

    response = llm.invoke(prompt)

    # Extract clean text reply
    reply = response.content.strip()
    print(f"🤖 Bot: {reply}")
    messages.append(f"Bot: {reply}")

    return {
        "messages": messages,
        "next": "update"
    }


# --------- Update Memory ---------
def update_memory(state: MemoryState) -> MemoryState:
    latest_bot_message = state["messages"][-1]
    vectorstore.add_texts([latest_bot_message])

    return {
        "messages": state["messages"],
        "next": "start"
    }


# --------- End Conversation ---------
def end_conversation(state: MemoryState) -> MemoryState:
    print("👋 Bot: Alright, take care! Ending conversation.")
    return {
        "messages": state["messages"]
    }


# --------- Build LangGraph ---------
builder = StateGraph(MemoryState)

builder.add_node("start", start_conversation)
builder.add_node("respond", retrieve_and_respond)
builder.add_node("update", update_memory)
builder.add_node("end", end_conversation)

builder.set_entry_point("start")

builder.add_conditional_edges(
    "start",
    lambda state: "end" if state["messages"][-1].lower().startswith("user: bye") or
                          state["messages"][-1].lower().startswith("user: exit") or
                          state["messages"][-1].lower().startswith("user: quit")
    else "respond"
)

builder.add_edge("respond", "update")
builder.add_edge("update", "start")
builder.add_edge("end", END)

graph = builder.compile()


# --------- Start Chat Loop ---------
initial_state = {
    "messages": [
        "User: I’ve been feeling anxious lately.",
        "Bot: I’m sorry to hear that. Want to talk more about it?",
        "User: Yeah, it’s mostly college stress.",
        "User: I feel stuck and unsure what to do next."
    ]
}

graph.invoke(initial_state)
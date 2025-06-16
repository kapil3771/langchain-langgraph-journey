import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import Dict, Any

from local_llm import LocalLLM
from memory import MemoryManager
from tools import tool_router

class ReActAgent:
    def __init__(self):
        self.llm = LocalLLM()
        self.memory = MemoryManager()

    def run(self, user_query: str) -> str:
        # 1. Store user message
        self.memory.store_message(f"User: {user_query}")

        # 2. Retrieve memory context (RAG style)
        context_docs = self.memory.retrieve_relevant(user_query)
        context_text = "\n".join([doc.page_content for doc in context_docs])

        # 3. Build initial prompt
        messages = [
            "You are a helpful AI agent that uses tools when needed.",
            f"Relevant Memory:\n{context_text}",
            f"User: {user_query}",
        ]

        # 4. Reasoning + Action loop
        for step in range(3):  # Max 3 steps
            agent_reply = self.llm.run(messages).strip()
            messages.append(f"Assistant: {agent_reply}")
            self.memory.store_message(f"Assistant: {agent_reply}")

            # Detect tool call: format = "Action: <tool_name>[<query>]"
            if agent_reply.lower().startswith("action:"):
                try:
                    tool_part = agent_reply.split(":", 1)[1].strip()
                    tool_name, query = tool_part.split("[", 1)
                    query = query.rstrip("]")
                    tool_name = tool_name.strip().lower()

                    # Run tool
                    observation = tool_router(tool_name, query)
                    messages.append(f"Observation: {observation}")
                    self.memory.store_message(f"Observation: {observation}")
                except Exception as e:
                    error_msg = f"❌ Tool parsing error: {e}"
                    messages.append(error_msg)
                    break
            else:
                # Final answer
                return agent_reply

        return "⚠️ I couldn't complete reasoning in time."
    
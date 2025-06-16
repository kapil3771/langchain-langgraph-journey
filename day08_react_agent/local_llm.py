# day08_react_agent/local_llm.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage
from langchain_core.messages import BaseMessage
from typing import List

class LocalLLM:
    def __init__(self, model_name: str = "gemma:2b"):
        self.llm = ChatOllama(model=model_name)

    def run(self, messages: List[BaseMessage]) -> str:
        response = self.llm.invoke(messages)
        return response.content


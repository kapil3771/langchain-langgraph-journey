import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import math 
import wikipedia
from typing import Dict
import ast
import operator


SAFE_MATH_FUNCS = {
    k: v for k, v in math.__dict__.items()
    if not k.startswith("__")
}
SAFE_MATH_FUNCS.update({
    "abs": abs,
    "round": round
})

def calculator_tool(query: str) -> str:
    """
    A secure calculator that supports math expressions and functions like sqrt, pow, abs, round.
    """
    try:
        # Evaluate using safe math context
        result = eval(query, {"__builtins__": {}}, SAFE_MATH_FUNCS)
        return f"🧮 {query.strip()} = {result}"
    except Exception as e:
        return f"❌ Calculator error: {str(e)}"
    
def wikipedia_tool(query: str) -> str:
    try:
        search_results = wikipedia.search(query)
        if not search_results:
            return f"❌ No Wikipedia results for: '{query}'"

        # Use first valid page
        for result in search_results:
            try:
                summary = wikipedia.summary(result, sentences=3)
                return f"📚 Wikipedia Summary for '{result}': {summary}"
            except (wikipedia.DisambiguationError, wikipedia.PageError):
                continue  # try next

        return f"❌ All search matches failed for: '{query}'"

    except Exception as e:
        return f"❌ Wikipedia Error: {e}"

def file_search_tool(query: str, search_dir = "documents/") ->str:
    try:
        if not os.path.exists(search_dir):
            return "📁 No document folder found."
        
        results = []
        for fname in os.listdir(search_dir):
            path = os.path.join(search_dir,fname)
            if os.path.isfile(path):
                with open(path,"r",encoding="utf-8",errors="ignore") as f:
                    content = f.read()
                    if query.lower() in content.lower():
                        results.append(f"✅ Found in: {fname}")

        if results:
            return "\n".join(results)
        else:
            return "🔍 No relevant files found."

    except Exception as e:
        return f"❌ File Search Error: {e}"
                
def tool_router(tool_name:str, query:str) ->str:
    tools = {
        "calculator":calculator_tool,
        "wikipedia":wikipedia_tool,
        "file_search": lambda q : file_search_tool(q)
    }
    tool_fn = tools.get(tool_name.lower())
    if tool_fn:
        return tool_fn(query)
    return "❌ Unknown tool requested."
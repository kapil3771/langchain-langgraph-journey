import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from langgraph.graph import StateGraph, END
from typing import TypedDict, List, Optional, Literal
from langchain_core.messages import BaseMessage
from pprint import pprint


class CRAGState(TypedDict):
    question: str
    retrieved_docs: List[str]
    grade: Literal["correct", "ambiguous", "incorrect"]
    feedback: str
    corrected_docs: Optional[List[str]]
    correction_reason: Optional[str]
    final_context: str
    answer: str
    logs: List[str]
    messages: List[BaseMessage]
    retry_count: int

def user_input_node(input: dict) -> CRAGState:
    question = input.get("question", "What is LangGraph?")
    return {
        "question": question,
        "retrieved_docs": [],
        "grade": "incorrect",
        "feedback": "",
        "corrected_docs": None,
        "correction_reason": None,
        "final_context": "",
        "answer": "",
        "logs": [f"📥 User input received: {question}"],
        "messages": [],
        "retry_count": 0
    }

from langchain_tavily import TavilySearch
os.environ["TAVILY_API_KEY"] = "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"

search_tool = TavilySearch(max_results = 3)

def retriever_node(state: CRAGState) -> CRAGState:
    question = state["question"]
    results = search_tool.invoke(question)

    if isinstance(results, dict) and "results" in results:
        docs = results["results"]
        text_snippets = [doc["content"] for doc in docs if "content" in doc]
    elif isinstance(results, list) and isinstance(results[0], dict) and "content" in results[0]:
        text_snippets = [doc["content"] for doc in results]
    elif isinstance(results, list) and isinstance(results[0], str):
        text_snippets = results
    else:
        text_snippets = [str(results)]

    logs = state["logs"] + [f"🔎 Retrieved {len(text_snippets)} documents."]

    return {
        **state,
        "retrieved_docs": text_snippets,
        "logs": logs
    }

from langchain_ollama import ChatOllama
llm = ChatOllama(model="gemma:2b")

def grading_node(state:CRAGState) ->CRAGState:
    question = state["question"]
    docs = state["retrieved_docs"]
    logs = state["logs"]
    retry_count = state.get("retry_count", 0) + 1

    prompt = f"""
You are a document quality evaluator for a QA system.

User asked:
{question}

Retrieved context:
{chr(10).join(docs)}

---

Evaluate the quality of the retrieved documents.
Return one of the following grades:
- correct → clearly answers the question
- incorrect → mostly irrelevant or wrong
- ambiguous → partial or unclear information

Also explain the reasoning in 1-2 lines.
Respond in JSON:
{{"grade": "...", "feedback": "..."}}
"""

    response = llm.invoke(prompt).content

    import json
    try:
        parsed = json.loads(response)
        grade = parsed.get("grade","incorrect").strip().lower()
        feedback = parsed.get("feedback", "No reasoning provided.").strip()
    except Exception:
        grade = "incorrect"
        feedback = "Failed to parse grading output."
    
    logs.append(f"🧪 Grading: {grade} — {feedback}")

    return {
        **state,
        "grade": grade,
        "feedback":feedback,
        "logs":logs,
        "retry_count": retry_count
    }

def correction_node(state:CRAGState) ->CRAGState:
    question = state["question"]
    retrieved = state["retrieved_docs"]
    grade = state["grade"]
    feedback = state["feedback"]
    logs = state["logs"]

    prompt = f"""
You're a retrieval correction assistant for a QA system.

The system failed to retrieve high-quality documents.

Original Question:
{question}

Retrieved (but low quality) Documents:
{chr(10).join(retrieved)}

Feedback from grader:
{feedback}

---

Please rewrite the search query or suggest a new strategy to improve document retrieval.
Respond ONLY in JSON:
{{"correction_reason": "...", "corrected_query": "..."}}
    """

    import json
    try:
        response = llm.invoke(prompt).content
        parsed = json.loads(response)
        corrected_query = parsed.get("corrected_query",question)
        correction_reason = parsed.get("correction_reason","Unknown reason")
    except Exception:
        corrected_query = question
        correction_reason = "Fallback: failed to parse correction."

    logs.append(f"🛠️ Correction: {correction_reason}")

    return{
        **state,
        "question":corrected_query,
        "correction_reason":correction_reason,
        "logs":logs
    }

def rerun_retrieval(state: CRAGState) -> CRAGState:
    corrected_query = state["question"]
    logs = state["logs"]

    results = search_tool.invoke(corrected_query)

    if isinstance(results, dict) and "results" in results:
        docs = results["results"]
        text_snippets = [doc["content"] for doc in docs if "content" in doc]
    elif isinstance(results, list) and isinstance(results[0], dict) and "content" in results[0]:
        text_snippets = [doc["content"] for doc in results]
    elif isinstance(results, list) and isinstance(results[0], str):
        text_snippets = results
    else:
        text_snippets = [str(results)]

    logs.append(f"📦 Retry retrieval complete: {len(text_snippets)} docs")

    return {
        **state,
        "retrieved_docs": text_snippets,
        "logs": logs
    }

def final_context_merge(state:CRAGState) -> CRAGState:
    docs = state["retrieved_docs"]
    logs = state["logs"]

    merged = "\n\n".join(docs)

    logs.append(f"📚 Final context merged from {len(docs)} documents.")

    return{
        **state,
        "final_context":merged,
        "logs":logs
    }

def answer_node(state: CRAGState) -> CRAGState:
    question = state["question"]
    context = state["final_context"]
    logs = state["logs"]

    prompt = f"""You are an expert assistant.

User Question:
{question}

Use the following context to answer:
{context}

If the context is insufficient, say "I don't know" or "Not enough information."
"""

    try:
        response = llm.invoke(prompt).content
    except Exception as e:
        response = f"❌ LLM Error: {str(e)}"

    logs.append("✅ Final answer generated.")

    return {
        **state,
        "answer": response,
        "logs": logs
    }

def ambiguous_merge(state: CRAGState) -> CRAGState:
    logs = state["logs"]
    retrieved = state["retrieved_docs"]
    feedback = state["feedback"]
    question = state["question"]

    merged_docs = retrieved + [feedback]

    logs.append("🔄 Ambiguous grade detected, merging docs and feedback, rerunning retrieval.")

    new_state = {
        **state,
        "retrieved_docs": merged_docs,
        "logs": logs
    }

    # Rerun retrieval with merged context as new query
    results = search_tool.invoke(question)

    if isinstance(results, dict) and "results" in results:
        docs = results["results"]
        text_snippets = [doc["content"] for doc in docs if "content" in doc]
    elif isinstance(results, list) and isinstance(results[0], dict) and "content" in results[0]:
        text_snippets = [doc["content"] for doc in results]
    elif isinstance(results, list) and isinstance(results[0], str):
        text_snippets = results
    else:
        text_snippets = [str(results)]

    logs.append(f"🔄 Ambiguous merge retrieval complete: {len(text_snippets)} docs")

    new_state.update({
        "retrieved_docs": text_snippets,
        "logs": logs
    })

    return new_state

def retry_limit_router(state: CRAGState) -> str:
    if state.get("retry_count", 0) >= 3:
        return "answer_node"
    return "grading"

graph = StateGraph(CRAGState)

graph.add_node("user_input", user_input_node)
graph.add_node("retriever", retriever_node)
graph.add_node("grading", grading_node)
graph.add_node("correction", correction_node)
graph.add_node("rerun_retrieval", rerun_retrieval)
graph.add_node("final_context_merge", final_context_merge)
graph.add_node("answer_node", answer_node)
graph.add_node("ambiguous_merge", ambiguous_merge)

def retry_router(state: CRAGState) -> str:
    if state["grade"] == "correct":
        return "final_context_merge"
    if state["grade"] == "ambiguous":
        return "ambiguous_merge"
    return "correction"

graph.add_edge("user_input", "retriever")
graph.add_edge("retriever", "grading")
graph.add_conditional_edges("grading", retry_router, {
    "final_context_merge": "final_context_merge",
    "correction": "correction",
    "ambiguous_merge": "ambiguous_merge"
})
graph.add_edge("correction", "rerun_retrieval")
graph.add_conditional_edges("rerun_retrieval", retry_limit_router, {
    "answer_node": "answer_node",
    "grading": "grading"
})
graph.add_edge("ambiguous_merge", "grading")
graph.add_edge("final_context_merge", "answer_node")
graph.set_entry_point("user_input")
graph.set_finish_point("answer_node")

os.environ["LANGCHAIN_API_KEY"] = "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"

import langsmith
langsmith_client = langsmith.Client()

app = graph.compile()

if __name__ == "__main__":
    config = {
    "configurable": {
        "thread_id": "crag_run_001"
    },
    "project_name": "CRAG LangGraph Project"
    }

    result = app.invoke({"question": "what is quantum computing?"}, config=config)
    pprint(result)

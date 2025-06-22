from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from state.selfrag_state import SelfRAGState

llm = ChatOllama(model="gemma:2b", temperature=0.3)

def answer_node(state: SelfRAGState) -> SelfRAGState:
    question = state.question
    context = state.final_context
    logs = state.logs

    prompt = f"""You are a helpful medical assistant.

Answer the user's question using only the context provided below.

Question:
{question}

Context:
{context}

If the context is insufficient, respond with "I don't know" or "Not enough information."
"""

    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        final_answer = response.content
    except Exception as e:
        final_answer = f"Error generating answer: {str(e)}"

    logs.append("Final answer generated.")

    updated_state = state.model_copy(update={
        "answer": final_answer,
        "logs": logs
    })

    return updated_state
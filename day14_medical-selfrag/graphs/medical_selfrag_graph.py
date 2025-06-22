from langgraph.graph import StateGraph, END
from state.selfrag_state import SelfRAGState
from nodes.user_input import user_input_node
from nodes.retriever import retriever_node
from nodes.rerun_retrieval import rerun_retrieval
from nodes.router import retry_router
from agents.grading_node import grading_node
from agents.corrector_node import corrector_node
from agents.trustrag_node import trustrag_node
from agents.context_merge_node import context_merge_node
from agents.answer_node import answer_node
from agents.hallucination_node import hallucination_node

def create_medical_selfrag_graph():
    """
    Creates the complete Medical Self-RAG graph with all nodes and routing logic
    """
    
    # Initialize the graph
    workflow = StateGraph(SelfRAGState)
    
    # Add all nodes
    workflow.add_node("user_input", user_input_node)
    workflow.add_node("retriever", retriever_node)
    workflow.add_node("grading", grading_node)
    workflow.add_node("trustrag", trustrag_node)
    workflow.add_node("corrector", corrector_node)
    workflow.add_node("rerun_retrieval", rerun_retrieval)
    workflow.add_node("context_merge", context_merge_node)
    workflow.add_node("answer_node", answer_node)
    workflow.add_node("hallucination_check", hallucination_node)
    
    # Set entry point
    workflow.set_entry_point("user_input")
    
    # Add edges
    workflow.add_edge("user_input", "retriever")
    workflow.add_edge("retriever", "grading")
    
    # Conditional routing after grading
    workflow.add_conditional_edges(
        "grading",
        retry_router,
        {
            "rerun_retrieval": "corrector",
            "context_merge": "trustrag",
            "answer_node": "context_merge"
        }
    )
    
    workflow.add_edge("corrector", "rerun_retrieval")
    workflow.add_edge("rerun_retrieval", "grading")
    workflow.add_edge("trustrag", "context_merge")
    workflow.add_edge("context_merge", "answer_node")
    workflow.add_edge("answer_node", "hallucination_check")
    
    # Final routing after hallucination check
    workflow.add_conditional_edges(
        "hallucination_check",
        lambda state: "corrector" if state.reflection_token == "ISREL_HALLUCINATED" and state.retry_count < 3 else END,
        {
            "corrector": "corrector",
            END: END
        }
    )
    
    return workflow.compile()

# Create the graph instance
graph = create_medical_selfrag_graph()
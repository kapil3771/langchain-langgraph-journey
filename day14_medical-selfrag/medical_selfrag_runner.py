import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
from graphs.medical_selfrag_graph import graph
from state.selfrag_state import SelfRAGState

def debug_graph_structure():
    """Debug the graph structure to see what nodes are available"""
    print("🔍 Debugging graph structure...")
    
    try:
        # Check if graph has nodes
        if hasattr(graph, 'nodes'):
            print(f"Graph nodes: {list(graph.nodes.keys())}")
        if hasattr(graph, 'edges'):
            print(f"Graph edges: {graph.edges}")
        if hasattr(graph, '_nodes'):
            print(f"Graph _nodes: {list(graph._nodes.keys())}")
        
        # Try to get graph info
        print(f"Graph type: {type(graph)}")
        print(f"Graph attributes: {dir(graph)}")
        
    except Exception as e:
        print(f"Error checking graph: {e}")

def test_individual_nodes():
    """Test individual nodes to see which ones work"""
    print("\n🧪 Testing individual nodes...")
    
    # Create a test state
    test_state = SelfRAGState(
        question="What is hypertension?",
        retrieved_docs=[],
        logs=["Starting test"]
    )
    
    try:
        # Test user_input node
        from nodes.user_input import user_input_node
        print("Testing user_input_node...")
        result = user_input_node(test_state)
        print(f"✅ user_input_node works: {len(result.logs)} logs")
        
    except Exception as e:
        print(f"❌ user_input_node failed: {e}")
    
    try:
        # Test retriever node
        from nodes.retriever import retriever_node
        print("Testing retriever_node...")
        result = retriever_node(test_state)
        print(f"✅ retriever_node works: {len(result.retrieved_docs)} docs retrieved")
        print(f"Logs: {result.logs}")
        
    except Exception as e:
        print(f"❌ retriever_node failed: {e}")
        import traceback
        print(traceback.format_exc())

def run_selfrag_debug(question: str):
    """
    Run the Medical Self-RAG system with detailed debugging
    """
    print(f"🚀 Starting Medical Self-RAG pipeline with question: {question}")
    
    # Debug graph structure first
    debug_graph_structure()
    
    # Test individual nodes
    test_individual_nodes()
    
    # Create input state manually
    print("\n📦 Creating input state...")
    input_state = SelfRAGState(
        question=question,
        retrieved_docs=[],
        logs=[f"Received user query: {question}"]
    )
    print(f"Input state created: {input_state}")
    
    try:
        # Execute graph with detailed logging
        print("\n🔄 Executing graph...")
        final_state = graph.invoke(input_state)
        
        print(f"\n✅ Graph execution completed!")
        print(f"Final state type: {type(final_state)}")
        print(f"Final state: {final_state}")
        
        # Display results with proper dictionary access
        print("\n" + "="*60)
        print("📥 Question:")
        print(question)
        
        # Fix: Use dictionary-style access for AddableValuesDict
        retrieved_docs = final_state.get('retrieved_docs', [])
        print(f"\n📚 Retrieved Docs ({len(retrieved_docs)}):")
        if retrieved_docs:
            for i, doc in enumerate(retrieved_docs):
                print(f"Doc {i+1}: {doc[:150]}{'...' if len(doc) > 150 else ''}\n")
        else:
            print("No documents retrieved.")

        final_context = final_state.get('final_context', '')
        print(f"\n🧠 Final Context:")
        if final_context:
            print(final_context[:500] + ('...' if len(final_context) > 500 else ''))
        else:
            print("No final context generated.")

        answer = final_state.get('answer', '')
        print(f"\n💬 Final Answer:")
        print(answer if answer else "No answer generated.")

        grade = final_state.get('grade', 'unknown')
        reflection_token = final_state.get('reflection_token', 'unknown')
        print(f"\n🎯 Grade & Reflection:")
        print(f"Grade: {grade.upper()}")
        print(f"Reflection Token: {reflection_token}")

        hallucination_spans = final_state.get('hallucination_spans', [])
        print(f"\n🚨 Hallucinations:")
        if hallucination_spans:
            for span in hallucination_spans:
                if span:
                    print(f"- {span}")
        else:
            print("None detected.")

        retry_count = final_state.get('retry_count', 0)
        print(f"\n🔄 Retry Information:")
        print(f"Total retries: {retry_count}")

        logs = final_state.get('logs', [])
        print(f"\n📜 Execution Logs ({len(logs)}):")
        if logs:
            for i, log in enumerate(logs):
                print(f"  {i+1}. {log}")
        else:
            print("No logs available.")

        print("="*60 + "\n")
        
        return final_state

    except Exception as e:
        print(f"\n❌ Error running Self-RAG pipeline: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print(f"Traceback:\n{traceback.format_exc()}")
        return None

def check_file_structure():
    """Check if all required files exist"""
    print("📁 Checking file structure...")
    
    required_files = [
        "graphs/medical_selfrag_graph.py",
        "state/selfrag_state.py",
        "nodes/user_input.py",
        "nodes/retriever.py",
        "embeddings/local_embedding_model.py",
        "vectorstore/faiss_index"
    ]
    
    for file_path in required_files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - MISSING!")
    
    # Check if FAISS index has files
    faiss_path = os.path.join(os.path.dirname(__file__), "vectorstore/faiss_index")
    if os.path.exists(faiss_path):
        files = os.listdir(faiss_path)
        print(f"📊 FAISS index files: {files}")
        if not files:
            print("⚠️  FAISS index directory is empty!")
    
    # Check if data directory has files
    data_path = os.path.join(os.path.dirname(__file__), "data/medical_docs")
    if os.path.exists(data_path):
        files = os.listdir(data_path)
        print(f"📄 Medical docs: {files}")
        if not files:
            print("⚠️  No medical documents found!")

def main():
    """
    Main function with comprehensive debugging
    """
    parser = argparse.ArgumentParser(description="Debug Medical Self-RAG System")
    parser.add_argument(
        "--question",
        type=str,
        default="What is hypertension?",
        help="Medical question to run through Self-RAG"
    )
    parser.add_argument(
        "--debug-only",
        action="store_true",
        help="Only run debugging checks, don't execute pipeline"
    )

    args = parser.parse_args()
    
    print(f"Current working directory: {os.getcwd()}")
    print(f"Script directory: {os.path.dirname(__file__)}")
    
    # Check file structure
    check_file_structure()
    
    if args.debug_only:
        print("🔍 Debug-only mode, skipping pipeline execution.")
        return
    
    # Run the Self-RAG system
    result = run_selfrag_debug(args.question)
    
    if result is None:
        print("❌ Pipeline failed to execute.")
        sys.exit(1)
    else:
        print("✅ Pipeline completed!")

if __name__ == "__main__":
    main()
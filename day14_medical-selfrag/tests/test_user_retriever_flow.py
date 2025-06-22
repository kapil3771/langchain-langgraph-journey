import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from nodes.user_input import user_input_node
from nodes.retriever import retriever_node
from pprint import pprint

if __name__ == "__main__":
    # 🟢 Simulate user question input
    state = user_input_node({"question": "What is hypertension?"})
    
    print("✅ After user_input_node:")
    pprint(state)
    print("\n" + "="*60 + "\n")

    # 🔍 Run FAISS retrieval
    state = retriever_node(state)

    print("✅ After retriever_node:")
    pprint({
        "retrieved_docs (snippet)": [doc[:100] + "..." for doc in state["retrieved_docs"]],
        "logs": state["logs"]
    })
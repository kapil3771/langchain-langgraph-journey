from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from pydantic import BaseModel
import os
from typing import List
import sqlite3

class MyState(BaseModel):
    value: int = 0
    logs: List[str] = []

def start_node(state: MyState) -> MyState:
    new_logs = state.logs + [f"Start with value = {state.value}"]
    return state.model_copy(update={"logs": new_logs})

def transform_node(state: MyState) -> MyState:
    new_logs = state.logs + ["Doubling the value"]
    new_value = state.value * 2
    return state.model_copy(update={"value": new_value, "logs": new_logs})

def end_node(state: MyState) -> MyState:
    new_logs = state.logs + [f"Final Value: {state.value}"]
    return state.model_copy(update={"logs": new_logs})

# Configuration
USE_SQLITE = False

if USE_SQLITE:
    # Ensure the checkpoints directory exists
    os.makedirs("checkpoints", exist_ok=True)
    # Create SqliteSaver with proper connection
    conn = sqlite3.connect("checkpoints/demo.db", check_same_thread=False)
    saver = SqliteSaver(conn)
    print("🗂️ Using SqliteSaver with file: checkpoints/demo.db")
else:
    saver = MemorySaver()
    print("⚡ Using MemorySaver (ephemeral)")

# Build the graph
builder = StateGraph(MyState)
builder.add_node("start", start_node)
builder.add_node("transform", transform_node)
builder.add_node("end", end_node)

builder.set_entry_point("start")
builder.add_edge("start", "transform")
builder.add_edge("transform", "end")
builder.add_edge("end", END)

graph = builder.compile(checkpointer=saver)

# Execute the graph
config = {"configurable": {"thread_id": "demo_thread_1"}}
final_state = graph.invoke(MyState(value=5), config=config)

print("\n✅ Execution complete.")

# Access the state correctly - final_state is a dictionary-like AddableValuesDict
# From debug output, we can see it's: {'value': 10, 'logs': [...]}
print(f"📊 Final Value: {final_state['value']}")
print("📝 Logs:")
for log in final_state['logs']:
    print(f"  • {log}")

# Replay history
print("\n🔄 Replaying history:")
try:
    history = list(graph.get_state_history(config))
    print(f"Found {len(history)} checkpoints")
    
    # Reverse to show in chronological order
    for i, checkpoint in enumerate(reversed(history)):
        if hasattr(checkpoint, 'values') and checkpoint.values:
            # checkpoint.values is the state dict
            state_data = checkpoint.values
            # Get the next step name if available
            next_steps = getattr(checkpoint, 'next', [])
            step_name = next_steps[0] if next_steps else 'end'
            
            # Access as dictionary
            if isinstance(state_data, dict):
                value = state_data.get('value', 'unknown')
                logs_count = len(state_data.get('logs', []))
            else:
                value = getattr(state_data, 'value', 'unknown')
                logs_count = len(getattr(state_data, 'logs', []))
                
            print(f"  Step {i+1}: {step_name} | State: value={value}, logs={logs_count} entries")
        else:
            print(f"  Step {i+1}: Checkpoint without values")
            
except Exception as e:
    print(f"  ⚠️ Could not retrieve history: {e}")
    print("  This might be due to LangGraph version differences or checkpoint format changes.")

print("\n🔍 Current state from checkpointer:")
try:
    current_state = graph.get_state(config)
    if current_state and hasattr(current_state, 'values'):
        state_values = current_state.values
        # Access as dictionary
        if isinstance(state_values, dict):
            value = state_values.get('value', 'unknown')
            logs = state_values.get('logs', [])
        else:
            value = getattr(state_values, 'value', 'unknown')
            logs = getattr(state_values, 'logs', [])
            
        print(f"  Current value: {value}")
        print(f"  Current logs: {len(logs)} entries")
        print("  All logs:")
        for i, log in enumerate(logs, 1):
            print(f"    {i}. {log}")
    else:
        print("  No current state found or state format unexpected")
except Exception as e:
    print(f"  ⚠️ Could not retrieve current state: {e}")
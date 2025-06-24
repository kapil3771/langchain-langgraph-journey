"""
Advanced LangGraph Checkpointing Demo with CLI Support

Features:
- Resume from specific checkpoint IDs
- Mid-run interruption and resumption
- Clean history visualization
- CLI interface for easy testing
- Support for both SQLite and Memory savers
"""

import argparse
import os
import sqlite3
import sys
import time
from typing import List, Optional, Dict, Any
from uuid import uuid4

from langgraph.graph import StateGraph, END
from langgraph.types import interrupt
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver
from pydantic import BaseModel


class MyState(BaseModel):
    value: int = 0
    logs: List[str] = []
    step_count: int = 0
    should_interrupt: bool = False


class CheckpointDemo:
    def __init__(self, use_sqlite: bool = True, db_path: str = "checkpoints/demo.db"):
        self.use_sqlite = use_sqlite
        self.db_path = db_path
        self.saver = self._create_saver()
        self.graph = self._build_graph()
    
    def _create_saver(self):
        """Create appropriate checkpointer based on configuration"""
        if self.use_sqlite:
            os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            saver = SqliteSaver(conn)
            print(f"🗂️ Using SqliteSaver with file: {self.db_path}")
            return saver
        else:
            print("⚡ Using MemorySaver (ephemeral)")
            return MemorySaver()
    
    def _build_graph(self):
        """Build the LangGraph with checkpointing"""
        builder = StateGraph(MyState)
        
        # Add nodes
        builder.add_node("start", self.start_node)
        builder.add_node("transform", self.transform_node)
        builder.add_node("process", self.process_node)
        builder.add_node("end", self.end_node)
        
        # Define edges
        builder.set_entry_point("start")
        builder.add_edge("start", "transform")
        builder.add_edge("transform", "process")
        builder.add_edge("process", "end")
        builder.add_edge("end", END)
        
        return builder.compile(checkpointer=self.saver)
    
    def start_node(self, state: MyState) -> MyState:
        """Initial node - sets up the computation"""
        new_logs = state.logs + [f"🚀 Starting computation with value = {state.value}"]
        new_step = state.step_count + 1
        print(f"  Step {new_step}: Starting with value {state.value}")
        
        return state.model_copy(update={
            "logs": new_logs,
            "step_count": new_step
        })
    
    def transform_node(self, state: MyState) -> MyState:
        """Transform node - doubles the value"""
        new_logs = state.logs + ["🔄 Transforming: Doubling the value"]
        new_value = state.value * 2
        new_step = state.step_count + 1
        print(f"  Step {new_step}: Doubling {state.value} → {new_value}")
        
        # Check if we should interrupt after this step
        if state.should_interrupt:
            print("  ⏸️ Interrupting execution after transform step...")
            interrupt("User requested interruption after transform")
        
        return state.model_copy(update={
            "value": new_value,
            "logs": new_logs,
            "step_count": new_step
        })
    
    def process_node(self, state: MyState) -> MyState:
        """Processing node - adds 10 to the value"""
        new_logs = state.logs + ["⚙️ Processing: Adding 10 to the value"]
        new_value = state.value + 10
        new_step = state.step_count + 1
        print(f"  Step {new_step}: Adding 10: {state.value} → {new_value}")
        
        return state.model_copy(update={
            "value": new_value,
            "logs": new_logs,
            "step_count": new_step
        })
    
    def end_node(self, state: MyState) -> MyState:
        """Final node - completion"""
        new_logs = state.logs + [f"✅ Computation complete! Final value: {state.value}"]
        new_step = state.step_count + 1
        print(f"  Step {new_step}: Finalizing with value {state.value}")
        
        return state.model_copy(update={
            "logs": new_logs,
            "step_count": new_step
        })
    
    def run_fresh(self, initial_value: int = 5, thread_id: Optional[str] = None, 
                  interrupt_after_transform: bool = False) -> tuple[Dict[str, Any], str]:
        """Run a fresh execution"""
        if thread_id is None:
            thread_id = f"demo_thread_{uuid4().hex[:8]}"
        
        config = {"configurable": {"thread_id": thread_id}}
        initial_state = MyState(
            value=initial_value,
            should_interrupt=interrupt_after_transform
        )
        
        print(f"\n🎯 Starting fresh execution with thread_id: {thread_id}")
        print(f"📊 Initial value: {initial_value}")
        
        try:
            final_state = self.graph.invoke(initial_state, config=config)
            print("\n✅ Execution completed successfully!")
            return final_state, thread_id
        except Exception as e:
            if "User requested interruption" in str(e):
                print(f"\n⏸️ Execution interrupted as requested: {e}")
                return self.get_current_state(thread_id), thread_id
            else:
                print(f"\n❌ Execution failed: {e}")
                raise
    
    def resume_from_checkpoint(self, thread_id: str, checkpoint_id: Optional[str] = None) -> Dict[str, Any]:
        """Resume execution from a specific checkpoint"""
        config = {"configurable": {"thread_id": thread_id}}
        
        if checkpoint_id:
            # Resume from specific checkpoint
            config["configurable"]["checkpoint_id"] = checkpoint_id
            print(f"\n🔄 Resuming from checkpoint: {checkpoint_id}")
        else:
            print(f"\n🔄 Resuming from latest checkpoint for thread: {thread_id}")
        
        try:
            # Get current state to resume from
            current_state = self.graph.get_state(config)
            if not current_state or not current_state.values:
                print("❌ No state found to resume from!")
                return {}
            
            # Resume execution - remove interrupt flag if it was set
            resume_state = MyState(**current_state.values)
            resume_state.should_interrupt = False
            
            final_state = self.graph.invoke(resume_state, config=config)
            print("\n✅ Resumed execution completed!")
            return final_state
            
        except Exception as e:
            print(f"\n❌ Resume failed: {e}")
            raise
    
    def get_current_state(self, thread_id: str) -> Dict[str, Any]:
        """Get the current state for a thread"""
        config = {"configurable": {"thread_id": thread_id}}
        try:
            current_state = self.graph.get_state(config)
            return current_state.values if current_state and current_state.values else {}
        except Exception as e:
            print(f"⚠️ Could not retrieve current state: {e}")
            return {}
    
    def display_history(self, thread_id: str, detailed: bool = False):
        """Display execution history for a thread"""
        config = {"configurable": {"thread_id": thread_id}}
        
        print(f"\n📜 Execution History for thread: {thread_id}")
        print("=" * 60)
        
        try:
            history = list(self.graph.get_state_history(config))
            if not history:
                print("  No history found.")
                return
            
            print(f"Found {len(history)} checkpoints")
            print()
            
            # Display in chronological order (reverse the list)
            for i, checkpoint in enumerate(reversed(history)):
                self._display_checkpoint(i + 1, checkpoint, detailed)
                
        except Exception as e:
            print(f"  ⚠️ Could not retrieve history: {e}")
    
    def _display_checkpoint(self, step_num: int, checkpoint, detailed: bool = False):
        """Display a single checkpoint"""
        if not hasattr(checkpoint, 'values') or not checkpoint.values:
            print(f"  Step {step_num}: Empty checkpoint")
            return
        
        state_data = checkpoint.values
        next_steps = getattr(checkpoint, 'next', [])
        checkpoint_id = getattr(checkpoint, 'config', {}).get('configurable', {}).get('checkpoint_id', 'unknown')
        
        # Extract state information
        if isinstance(state_data, dict):
            value = state_data.get('value', 'unknown')
            logs_count = len(state_data.get('logs', []))
            step_count = state_data.get('step_count', 0)
        else:
            value = getattr(state_data, 'value', 'unknown')
            logs_count = len(getattr(state_data, 'logs', []))
            step_count = getattr(state_data, 'step_count', 0)
        
        next_step = next_steps[0] if next_steps else 'END'
        
        print(f"  📍 Checkpoint {step_num}:")
        print(f"     ID: {checkpoint_id}")
        print(f"     Next: {next_step}")
        print(f"     State: value={value}, step_count={step_count}, logs={logs_count} entries")
        
        if detailed and isinstance(state_data, dict) and state_data.get('logs'):
            print(f"     Logs:")
            for log in state_data['logs']:
                print(f"       • {log}")
        print()
    
    def list_available_threads(self):
        """List all available thread IDs (SQLite only)"""
        if not self.use_sqlite:
            print("⚠️ Thread listing only available with SQLite saver")
            return []
        
        try:
            # Query the database directly to find available threads
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT thread_id FROM checkpoints ORDER BY thread_id")
            threads = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            if threads:
                print("\n📋 Available threads:")
                for thread in threads:
                    print(f"  • {thread}")
            else:
                print("\n📋 No threads found in database")
            
            return threads
        except Exception as e:
            print(f"⚠️ Could not list threads: {e}")
            return []


def main():
    parser = argparse.ArgumentParser(description="Advanced LangGraph Checkpointing Demo")
    parser.add_argument("--value", type=int, default=5, help="Initial value for computation")
    parser.add_argument("--thread-id", type=str, help="Thread ID to use or resume")
    parser.add_argument("--checkpoint-id", type=str, help="Specific checkpoint ID to resume from")
    parser.add_argument("--resume", action="store_true", help="Resume from existing checkpoint")
    parser.add_argument("--interrupt", action="store_true", help="Interrupt after transform step")
    parser.add_argument("--history", action="store_true", help="Show execution history")
    parser.add_argument("--detailed-history", action="store_true", help="Show detailed execution history")
    parser.add_argument("--list-threads", action="store_true", help="List available threads")
    parser.add_argument("--memory", action="store_true", help="Use memory saver instead of SQLite")
    parser.add_argument("--db-path", type=str, default="checkpoints/demo.db", help="SQLite database path")
    
    args = parser.parse_args()
    
    # Create demo instance
    demo = CheckpointDemo(use_sqlite=not args.memory, db_path=args.db_path)
    
    # Handle different operations
    if args.list_threads:
        demo.list_available_threads()
        return
    
    if args.history or args.detailed_history:
        if not args.thread_id:
            print("❌ --thread-id required for history display")
            return
        demo.display_history(args.thread_id, detailed=args.detailed_history)
        return
    
    if args.resume:
        if not args.thread_id:
            print("❌ --thread-id required for resume operation")
            return
        
        final_state = demo.resume_from_checkpoint(args.thread_id, args.checkpoint_id)
        if final_state:
            print(f"\n📊 Final State:")
            print(f"  Value: {final_state.get('value', 'unknown')}")
            print(f"  Steps completed: {final_state.get('step_count', 'unknown')}")
    else:
        # Fresh execution
        final_state, thread_id = demo.run_fresh(
            initial_value=args.value,
            thread_id=args.thread_id,
            interrupt_after_transform=args.interrupt
        )
        
        if final_state:
            print(f"\n📊 Final State:")
            print(f"  Thread ID: {thread_id}")
            print(f"  Value: {final_state.get('value', 'unknown')}")
            print(f"  Steps completed: {final_state.get('step_count', 'unknown')}")
            
            if args.interrupt:
                print(f"\n💡 To resume: python {sys.argv[0]} --resume --thread-id {thread_id}")


if __name__ == "__main__":
    main()
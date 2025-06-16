import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from day08_branching_agent.intent_classifier import classify_intent
from day08_branching_agent.memory import MemoryManager

# Optional tools
from datetime import datetime

# Initialize persistent memory
memory = MemoryManager()

def handle_chitchat(message: str) -> str:
    # Simple hardcoded small talk replies
    if "how are you" in message.lower():
        return "I'm doing great! Thanks for asking. 😊"
    elif "good morning" in message.lower():
        return "Good morning to you too! 🌞"
    elif "hello" in message.lower():
        return "Hey there! 👋"
    else:
        return "Nice talking to you! 😄"

def handle_task(message: str) -> str:
    # Placeholder for task logic - simulate processing
    # This is where tools like calculator, Wikipedia etc. will be added later
    if "time" in message.lower():
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}."
    return f"I'm working on your task: '{message}'."

def branching_agent(message: str) -> dict:
    intent = classify_intent(message)
    
    if intent == "chitchat":
        response = handle_chitchat(message)
    else:
        response = handle_task(message)

    # Save conversation in memory
    memory.add(f"User: {message}\nAgent: {response}", metadata={"intent": intent})

    return {
        "intent": intent,
        "response": response
    }

# Quick test if run directly
if __name__ == "__main__":
    user_input = input("You: ")
    result = branching_agent(user_input)
    print(f"[Intent: {result['intent']}]")
    print(f"Agent: {result['response']}")
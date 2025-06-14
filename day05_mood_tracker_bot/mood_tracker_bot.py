from langgraph.graph import StateGraph, END
from pydantic import BaseModel
from langchain_core.runnables import RunnableLambda
from typing import List

class MoodState(BaseModel):
    mood: str = ""
    mood_history: List[str] = []

def start(state: MoodState) -> MoodState:
    print("🤖 Bot: How are you feeling today?")
    user_input = input("👤 You: ")
    return MoodState(mood=user_input, mood_history=state.mood_history)

def analyze_mood(state: MoodState) -> MoodState:
    mood = state.mood.lower()
    state.mood_history.append(mood)
    return state

def respond(state: MoodState) -> MoodState:
    mood = state.mood.lower()
    if "happy" in mood:
        print("😊 That's wonderful to hear!")
    elif "sad" in mood:
        print("💙 I'm here for you.")
    elif "anxious" in mood or "stressed" in mood:
        print("🧘 Let's take a deep breath together.")
    else:
        print("🤖 Thank you for sharing how you feel.")
    return state

def summary(state: MoodState) -> MoodState:
    print("📊 Mood Summary:", state.mood_history)
    return state

builder = StateGraph(MoodState)

builder.add_node("start", RunnableLambda(start))
builder.add_node("analyze_mood", RunnableLambda(analyze_mood))
builder.add_node("respond", RunnableLambda(respond))
builder.add_node("summary", RunnableLambda(summary))

builder.set_entry_point("start")
builder.set_finish_point("summary")

builder.add_edge("start", "analyze_mood")
builder.add_edge("analyze_mood", "respond")
builder.add_edge("respond", "summary")

app = builder.compile()
app.invoke(MoodState())  # Start with an empty state
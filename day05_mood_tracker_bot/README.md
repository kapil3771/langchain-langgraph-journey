# 🧠 Day 5: Mood Tracker Bot — Custom State with Pydantic

Welcome to **Day 5** of the LangGraph Journey! Today’s focus is on **custom state management** using `Pydantic`, and building a conversational agent that tracks user mood throughout the conversation.

---

## 📌 Topics Covered

- ✅ Defining custom state using `pydantic.BaseModel`
- ✅ Persisting state across LangGraph nodes
- ✅ Updating and mutating state via `return {...}`
- ✅ Clean flow design with state-driven logic

---

## 🎯 Project Goal

Build a **Mood Tracker Bot** that:

- Asks how the user feels
- Stores their mood
- Tracks mood history
- Responds empathetically
- Summarizes mood at the end

---

## 🔧 Tech Stack

- Python 🐍
- LangGraph ⚙️
- Pydantic 🧬
- LangChain Core (RunnableLambda)

---

## 🧠 State Model

We use a `MoodState` Pydantic model:

```python
from pydantic import BaseModel
from typing import List

class MoodState(BaseModel):
    mood: str = ""
    mood_history: List[str] = []
```

---

## 📊 Flow Overview

```text
start → analyze_mood → respond → summary (END)
```

### 🧩 Node Functions:

| Node            | Description                               |
|------------------|-------------------------------------------|
| `start`          | Prompt user for mood input                |
| `analyze_mood`   | Append mood to history                    |
| `respond`        | Respond based on emotional context        |
| `summary`        | Show all moods tracked so far             |

---

## 💡 Example Interaction

```text
🤖 Bot: How are you feeling today?
👤 You: I'm feeling anxious.

🧘 Let's take a deep breath together.
📊 Mood Summary: ['anxious']
```

---

## 🧠 Learning Outcome

By completing Day 5, you’ve learned:

- How to manage complex state with Pydantic
- How to carry that state across nodes
- How to build emotionally aware, stateful agents
- How LangGraph tracks and mutates state cleanly

---

## 📂 Files

| File                | Description                            |
|---------------------|----------------------------------------|
| `mood_tracker_bot.py` | Full LangGraph + Pydantic implementation |
| `README.md`          | Documentation and usage guide         |

---


_💙 Made with curiosity and LangGraph._
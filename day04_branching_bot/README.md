# 📍 Day 4 – Branching Support Bot using LangGraph

### 🔧 Concepts Covered:
- `set_entry_point()` – Define where the graph starts
- `set_finish_point()` – Define valid terminal nodes
- `add_conditional_edges()` – Add IF/ELSE type logic between nodes
- Custom routing logic using Python functions
- Typed state definition using `TypedDict`
- Building a multi-path decision system using LangGraph

---

### 🤖 Project: Branching Support Bot

This bot asks for a user query and routes to:
- 💳 Billing Support – if query contains "billing" or "payment"
- 🛠️ Tech Support – if query contains "technical" or "tech"
- 🤷 Fallback – for anything else

---

### 📁 Files:
- `branching_bot.py` – The main graph definition and bot logic

---

### ▶️ Run:
```bash
cd day04_branching_bot
python branching_bot.py
```

---

### ✅ Example:
```
🤖 Bot: Hi! How can I help you today?
👤 You: I have a billing issue
💳 Billing: I can help you with billing issues.
```

---

### 🔍 Learnings:
This shows how LangGraph handles decision trees using conditional edges. You can map string outputs to specific paths using a custom `route()` function. Each node is pure and stateless, and the graph handles flow control.
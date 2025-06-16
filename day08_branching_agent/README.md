# 🧠 Day 8: Branching Memory Agent with FAISS + Gradio UI

This project demonstrates a **Branching Agent** using LangGraph that:
- Classifies user intent (`chitchat` vs `task`)
- Routes conversation logic accordingly
- Stores multi-turn memory in a **FAISS vectorstore** using a **local MiniLM embedding model**
- Presents everything via a **modern Cyberpunk-styled Gradio UI**

---

## 🚀 Features

### ✅ Intent Branching
- Uses a simple keyword-based classifier to detect `chitchat` vs `task`
- Dynamically routes message handling in a LangGraph flow

### ✅ Persistent Memory
- FAISS vectorstore stores conversation turns with semantic embeddings
- Embedding done locally using: `sentence-transformers/all-MiniLM-L6-v2`

### ✅ Modular Design
- Cleanly separated modules:
  - `intent_classifier.py` → classifies intent
  - `memory.py` → manages FAISS index
  - `branching_agent.py` → classic function-based agent
  - `graph.py` → LangGraph implementation
  - `ui.py` → Gradio interface with memory preview

### ✅ Beautiful Gradio UI
- Cyberpunk-themed chat interface
- Emoji branding
- Live FAISS memory preview

---

## 🧩 Folder Structure

```
day08_branching_agent/
├── branching_agent.py        # Classic branching logic
├── graph.py                  # LangGraph version of branching agent
├── intent_classifier.py      # Rule-based intent classifier
├── memory.py                 # FAISS memory manager
├── ui.py                     # Gradio frontend with dark theme + memory
└── README.md                 # You’re here
```

---

## ⚙️ Requirements

Install dependencies in your Python virtual environment:

```bash
pip install -r requirements.txt
```

Minimal requirements:

```txt
langgraph
langchain
faiss-cpu
sentence-transformers
gradio
```

Make sure you have:
- ✅ [Ollama installed](https://ollama.com/)
- ✅ The `all-MiniLM-L6-v2` model downloaded locally

---

## 🧪 Run Tests

To run the basic agent:

```bash
python day08_branching_agent/branching_agent.py
```

To run LangGraph version:

```bash
python day08_branching_agent/graph.py
```

To launch Gradio UI:

```bash
python day08_branching_agent/ui.py
```

---

## 🧠 Example Output

```txt
You: what's the time?
[Intent: task]
Agent: The current time is 16:45:12.

🧠 FAISS Memory:
🔹 User: what's the time?
   Agent: The current time is 16:45:12.
```

---

## 🌱 Future Ideas

- 🔀 Switch intent classifier to LLM (e.g., via Gemma 2B)
- 🧩 Add actual tools for task nodes (calculator, Wikipedia, file search)
- 🧠 Visualize FAISS memory graphically
- 🗂️ Export memory as markdown or JSON
- 🧬 Extend graph into multi-agent interaction

---

## 💡 Core Learning

✅ This project teaches how to:
- Design modular agent systems with intent branching
- Integrate LangGraph with local embeddings and FAISS
- Build elegant UIs for agent workflows
- Implement semantic memory that persists across sessions

---

## 🧠 Credits

Developed as part of the **Advanced LangGraph Curriculum - Day 8**  
Uses local stack: `Gemma 2B` (future), `MiniLM`, `FAISS`, `Gradio`, and `LangGraph`.

---

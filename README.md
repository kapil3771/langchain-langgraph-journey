# 🌐 LangChain + LangGraph Journey 🚀

This project is a 30-day hands-on learning journey where I (Kapil) explore and master **LangGraph** to build powerful, production-grade AI agents using **LangChain** and Python.

Each day focuses on a new concept — with detailed code, explanations, and real projects from scratch to advanced memory & checkpointing systems.

---

## 📚 Project Structure

```bash
langchain-langgraph-journey/
├── day01_setup_installation/         # LangGraph + LangChain install & setup
├── day02_echo_node/                  # First echo bot with simple graph
├── day03_step_flow/                  # Multi-step flow using node chaining
├── day04_branching_bot/             # Conditional branching logic
├── day05_mood_tracker_bot/          # Custom state & mood tracking with Pydantic
├── day06_personality_test/          # Multi-step personality quiz bot
├── day07_memory_agent/              # Local memory + FAISS + local LLM
├── day08_branching_agent/           # Advanced branching with memory & UI
├── day08_react_agent/               # ReAct agent with tool use and memory
├── day09_doc_analysis_bot.py        # LangGraph + Ollama document Q&A
├── day10_Self-Evaluating...         # Self-evaluating cyclic Q&A agent
├── day11_retry_workflows/           # Retry-until-correct logic with grading
├── day12_multi_agent/               # Multi-agent orchestration via LangGraph
├── day13_crag_agent/                # CRAG agent with memory and self-eval
├── day14_medical-selfrag/           # Full Self-RAG pipeline on medical docs
├── day15_persistence_memory/        # ✅ Advanced checkpointing (InMemory, Sqlite)
├── documents/                       # PDFs, text files for ingestion
├── embeddings/                      # FAISS indexes
├── requirements.txt                 # All dependencies
└── README.md                        # You are here 📖
```

---

## 🔍 Highlighted Milestones

| Day | Title | Highlights |
|-----|-------|------------|
| 2 | Echo Bot | First LangGraph hello world |
| 4 | Branching Bot | Conditional logic based on state |
| 5 | Mood Tracker | Custom state handling |
| 7 | Memory Agent | Memory, vector DB, local LLM |
| 8 | ReAct Agent | Tool use, branching, UI |
| 10 | Self-Eval QA Agent | Cyclical loop + retry |
| 12 | Multi-Agent | Agent coordination |
| 14 | 🩺 Medical Self-RAG | Real-world QA + FAISS + trust layer |
| 15 | 💾 Persistence | Sqlite + thread resume + time travel |

---

## 🧪 How to Run Demos

### ✅ Setup

```bash
git clone https://github.com/kapil3771/langchain-langgraph-journey.git
cd langchain-langgraph-journey
pip install -r requirements.txt
```

### ✅ Run Advanced Checkpointing Demo (Day 15)

```bash
cd day15_persistence_memory
python adv_checkpointing_demo.py                     # Normal run
python adv_checkpointing_demo.py --resume            # Resume from last checkpoint
python adv_checkpointing_demo.py --resume \
  --thread-id demo_thread_123 --checkpoint-id xyz    # Resume specific run
```

---

## 📤 Push to GitHub

After updating files:

```bash
git add .
git commit -m "✅ Add Day 15 - Checkpointing + README update"
git push origin main
```

---

## 🧠 Concepts Mastered So Far

- LangGraph: `StateGraph`, `add_node`, `add_conditional_edges`, `END`
- Pydantic-based state design
- Memory: FAISS, local storage, and retrieval
- Retry workflows using LLM-as-Judge
- Agentic orchestration (ReAct, CRAG)
- Persistence: `InMemorySaver`, `SqliteSaver`, `get_state_history`
- Time-travel debugging and thread replay
- Self-RAG with hallucination detection and answer scoring

---

## 🤖 Final Goals (WIP)

- ✅ Build a production-grade Medical QA Self-RAG Agent
- ✅ Enable stateful retry & filtering using LangGraph
- ✅ Implement time-travel memory and history debugging
- ⏳ Add evaluation + UI polish (Week 8+)

---

Built with ❤️ by Kapil 
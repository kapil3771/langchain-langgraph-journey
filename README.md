# 🌐 LangChain + LangGraph Journey 🚀

This project is a 30-day hands-on learning journey where I (Kapil) explore and master **LangGraph** to build powerful, production-grade AI agents using **LangChain** and Python.

Each day focuses on a new concept — with detailed code, explanations, and real project files stored in folders like `day01_setup_installation/`, `day02_echo_node/`, and so on.

---

## 🔧 Environment Setup & Installation

Follow these steps to set up and activate the isolated Python environment for this project.

### ✅ 1. Clone the Repository

```bash
git clone https://github.com/kapil3771/langchain-langgraph-journey.git
cd langchain-langgraph-journey
```

### ✅ 2. Create a Virtual Environment

```bash
python3 -m venv langgraph-env
```

### ✅ 3. Activate the Virtual Environment

**On macOS/Linux:**
```bash
source langgraph-env/bin/activate
```

**On Windows (CMD):**
```cmd
langgraph-env\Scripts\activate.bat
```

**On Windows (PowerShell):**
```powershell
.\langgraph-env\Scripts\Activate.ps1
```

### ✅ 4. Install Dependencies

```bash
pip install -r requirements.txt
```

Or, if starting fresh:

```bash
pip install langgraph langchain openai
pip freeze > requirements.txt
```

### ✅ 5. Run Code

Navigate to any day's directory and run the script:

```bash
cd day02_echo_node
python echo_bot.py
```

> 💡 Make sure the virtual environment is activated **before running any script**.

---

## 📁 Folder Structure

```
langchain-langgraph-journey/
├── langgraph-env/           # 🔒 Isolated virtual environment (ignored in git)
├── day01_setup_installation/
├── day02_echo_node/
├── day03_step_flow/
├── day04_conditional_branching/
├── day05_tool_using_agent/
├── day06_memory_basics/
├── day07_multi_turn_memory_agent/
├── day08_branching_agent/
├── requirements.txt         # 📦 Pinned dependencies
├── .gitignore               # 🚫 Files and folders to ignore in Git
└── README.md                # 📘 You’re reading it!
```

---

## 📅 Progress Tracking

| Day  | Topic                                          | Status            |
|------|------------------------------------------------|-------------------|
| 01   | LangGraph Installation                         | ✅ Done            |
| 02   | Echo Node + StateGraph                         | ✅ Done            |
| 03   | Step Flows                                     | ✅ Mastered        |
| 04   | Conditional Branching                          | ✅ Mastered        |
| 05   | Tool-using Agents                              | ✅ Done            |
| 06   | Memory Basics (Stateful Agent)                 | ✅ Done            |
| 07   | Multi-turn Memory Agent + FAISS                | ✅ Mastered        |
| 08.1 | Branching Agent (Classic + Graph + Gradio UI)  | ✅ Completed       |
| 08.2 | ReAct Agent with LangGraph                     | 🔜 Next up         |
| ...  | ...                                            | 🔜 Coming Soon     |

---

## 🤝 Contributions

This is a personal learning repository, but feel free to fork it, star it, and suggest improvements!

---

## 📜 License

MIT License. Use and learn freely 🙌
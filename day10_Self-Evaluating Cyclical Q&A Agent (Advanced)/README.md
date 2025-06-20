# 🤖 Self-Evaluating Cyclical Q&A Agent

This project demonstrates a **LangGraph-based intelligent agent** that can **generate answers to questions, self-evaluate using an LLM-based grader, and retry until confident**, with a fallback for poor answers. The agent is fully local using [Ollama](https://ollama.com/) and the OpenChat model.

---

## 🚀 Core Functionality

- **Cyclical retry loop**: Automatically retries if the generated answer doesn't score well.
- **LLM-based grading**: Uses a second LLM call to judge the quality of the answer.
- **Auto-routing logic**: Uses conditional edges to loop or fallback based on grading.
- **Debug logs**: Every step logs actions for traceability and debugging.
- **Local-first**: Entirely runs on your machine using Ollama (no external API calls).

---

## 🧱 Architecture / Concepts

| Component | Description |
|----------|-------------|
| `EvalState` | The shared state between graph nodes (question, answer, score, retries, logs, debug flag) |
| `@entrypoint` | Entry node of the graph — initializes the process |
| `@task` nodes | Stateless function nodes that generate answers, grade them, and fallback |
| `router()` | Decision logic to control looping or exit |
| `StateGraph` | LangGraph's orchestration engine — builds the full agent logic graph |
| `Ollama` | Local LLM execution backend (using OpenChat model) |

---

## 🛠️ Tech Stack / Libraries Used

- **[LangGraph](https://github.com/langchain-ai/langgraph)** (`v0.4.8`): For stateful graph-based LLM workflows
- **[LangChain-Ollama](https://python.langchain.com/docs/integrations/llms/ollama/)**: Interface to local models
- **[Python 3.10+]**
- **OpenChat (via Ollama)**: Local chat model with high-quality performance

---

## 🧪 Example Usage

```python
# Example input to the compiled graph:
inputs = {
    "question": "What is the capital of France?",
    "retries": 0,
    "logs": [],
    "debug": True
}

# Run the graph
result = graph.invoke(inputs)
print(result["answer"])
print(result["logs"])
```

Output:
```
Paris
['Starting question answering...', 'Generated Answer: Paris', 'Grading result: 1.0 (Retry 1)', 'Score high enough, finishing.']
```

---

## ✅ What You Learn

- How to design a **stateful multi-step LLM agent** using LangGraph
- How to integrate **grading logic into loops** for self-improving agents
- How to use **conditional edges** for graph control
- Running LLMs **entirely locally using Ollama**
- Building **robust retry and fallback mechanisms**

---

## 📂 File Structure

```
├── Agent.py         # Main LangGraph agent logic
├── README.md        # Project overview and usage
```

---

## 💡 Future Ideas

- Add **streaming output** using `llm.stream()`
- Use **MemorySaver** to checkpoint state across runs
- Allow **human-in-the-loop correction** before fallback

---

## 🧠 Inspiration

This project is part of a GenAI learning journey focused on **LangGraph mastery** and building intelligent autonomous agents.
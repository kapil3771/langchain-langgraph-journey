# LangChain LangGraph Journey 🚀

A personal journey into building real-world, production-ready applications using **LangGraph**, **LangChain**, and **local models** like **Gemma 2B** and **MiniLM**. This repo is structured day-by-day to deepen mastery through hands-on coding and real use cases.

---

## ✅ Stack

- 🧠 **LLM**: [Gemma 2B](https://ollama.com/library/gemma) via [Ollama](https://ollama.com/)
- 📎 **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
- 📂 **Vector Store**: FAISS (local, persistent)
- 🧩 **Framework**: LangGraph + LangChain
- 💻 **UI**: Gradio (chatbot wrapper)
- 💾 **Local Only**: 100% local inference, no API keys required

---

## 📅 Day 7 – Multi-Turn Memory Agent with Local Stack

### 🔍 Features

- Multi-turn **conversational memory** using FAISS
- LangGraph agent built with **state management**
- Uses **local embeddings** + **local LLM** for context-aware replies
- Automatic **FAISS save/load** on each chat
- Basic **Gradio UI wrapper**

### ▶️ To Run

```bash
# 1. Activate your virtual environment
source langgraph-env/bin/activate

# 2. Run the chatbot
python day07_memory_agent/memory_agent.py
```

Make sure you have `ollama` running Gemma 2B:
```bash
ollama run gemma:2b
```



## 🛠 Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

> Make sure to install:
> - `langchain`
> - `langgraph`
> - `sentence-transformers`
> - `faiss-cpu`
> - `langchain_community`
> - `langchain_ollama`

---


## 🙌 Author

**Kapil** – AIDS Engineering Student & GenAI Developer  
Building open-source AI agents with LangGraph + Local Stack

---

## ⭐️ Star this repo if you find it useful!
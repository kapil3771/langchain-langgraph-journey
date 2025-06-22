# 🧠 Medical Self-RAG System with LangGraph

![LangGraph Version](https://img.shields.io/badge/langgraph-0.4.8-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Production--Ready-success)

---

## 📌 Project Overview

This project implements a **production-grade Self-RAG (Reflective Retrieval-Augmented Generation)** system for medical question-answering using [LangGraph](https://github.com/langchain-ai/langgraph), local LLMs (Gemma 2B via Ollama), and FAISS-based vector search.

### 🔍 Problem It Solves

Traditional RAG systems often return **incomplete or hallucinated answers** because they:
- Use fixed retrieval pipelines
- Fail to correct or reflect on low-quality context
- Lack trust filtering (e.g., CDC/NIH vs random blogs)

This Self-RAG system solves those issues by introducing:

| Feature | Description |
|--------|-------------|
| 🔁 **Self-Reflection Loop** | Dynamically re-routes based on grading + reflection |
| 🧪 **Hallucination Detection** | Flags ungrounded answer spans |
| 🧠 **Correction & Retry** | Automatically rewrites poor queries |
| 🧯 **TrustRAG Filtering** | Prioritizes reliable sources |
| 💬 **Final Merged Context** | Synthesizes best available info before answering |

---

## 🔗 System Architecture

```mermaid
graph LR
A[User Input] --> B[Retriever]
B --> C[TrustRAG Filter]
C --> D[Grader]
D --> E{Router (Retry Logic)}
E -->|ISREL| F[Corrector + Rerun Retrieval]
E -->|ISSUP| G[Context Merger]
E -->|ISUSE| I[Answer Node]
E -->|correct| I[Answer Node]
G --> I
F --> D
I --> J[Hallucination Detector]
J --> K((END))
```

---

## 🧰 Tech Stack

| Component | Tool |
|----------|------|
| Language | Python 3.10+ |
| Orchestration | LangGraph 0.4.8 |
| LLM | Ollama Gemma:2B |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` |
| Vector DB | FAISS |
| Docs | Local medical PDFs and .txts |

---

## 🚀 How to Run

1. **Clone Repo & Create Virtual Env**  
```bash
git clone https://github.com/kapil3771/langchain-langgraph-journey/tree/main/day14_medical-selfrag.git
cd medical-selfrag
python -m venv langgraph-env
source langgraph-env/bin/activate
pip install -r requirements.txt
```

2. **Ingest Documents into FAISS**
```bash
python ingest/ingest_faiss.py
```

3. **Run Self-RAG Pipeline**
```bash
python medical_selfrag_runner.py --question "What is hypertension?"
```

---

## 📂 Project Structure

```
day14_medical-selfrag/
├── agents/                  # Core agent nodes (LLM-based)
├── embeddings/              # Embedding model wrapper
├── graphs/                  # LangGraph orchestration
├── ingest/                  # FAISS ingestion scripts
├── nodes/                   # Non-agent nodes (retriever, router)
├── state/                   # Pydantic state model
├── vectorstore/             # FAISS index storage
├── tests/                   # Test files for nodes/agents                   
└── medical_selfrag_runner.py
```


---

## 🧠 Author Notes

This system demonstrates **full-loop autonomous correction, retrieval grading, and hallucination detection**.

Ideal for: 🔬 medical QA, 📚 academic assistants, 🧠 multi-agent research systems.

---

© 2025 Medical Self-RAG by Kapil — All Rights Reserved.
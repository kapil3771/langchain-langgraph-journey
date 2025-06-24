# 🚀 Advanced LangGraph Checkpointing Demo

A fully-featured CLI demo to explore advanced checkpointing capabilities using **LangGraph**.

---

## 🧠 Features

- ✅ Fresh runs with custom initial state
- ✅ Mid-run interruption and resume support
- ✅ Resume from latest or specific checkpoint ID
- ✅ View execution history and detailed logs
- ✅ List all saved thread IDs (SQLite only)
- ✅ Toggle between `MemorySaver` and `SqliteSaver`
- ✅ Clean CLI interface for experimentation

---

## 📦 Requirements

- Python 3.8+
- `langgraph` installed (0.4.8+)
- Pydantic 2.x
- SQLite (default) or in-memory support

---

## ▶️ Usage: Test Commands

### 🚀 1. Fresh Run (Default Value = 5)
```bash
python adv_checkpointing_demo.py
```

### 🎯 2. Fresh Run with Custom Initial Value
```bash
python adv_checkpointing_demo.py --value 10
```

### ⏸️ 3. Fresh Run with Interruption After Transform
```bash
python adv_checkpointing_demo.py --value 7 --interrupt
```

### 🔄 4. Resume from Latest Checkpoint (After Interrupt)
```bash
python adv_checkpointing_demo.py --resume --thread-id <THREAD_ID>
```

### 📍 5. Resume from Specific Checkpoint ID
```bash
python adv_checkpointing_demo.py --resume --thread-id <THREAD_ID> --checkpoint-id <CHECKPOINT_ID>
```

### 📜 6. Show Execution History
```bash
python adv_checkpointing_demo.py --history --thread-id <THREAD_ID>
```

### 📝 7. Show Detailed Execution History (Logs Included)
```bash
python adv_checkpointing_demo.py --detailed-history --thread-id <THREAD_ID>
```

### 📋 8. List All Available Threads (SQLite Only)
```bash
python adv_checkpointing_demo.py --list-threads
```

### ⚡ 9. Use In-Memory Saver Instead of SQLite (Ephemeral)
```bash
python adv_checkpointing_demo.py --memory
```

### 🗂️ 10. Use Custom SQLite DB Path
```bash
python adv_checkpointing_demo.py --db-path checkpoints/my_custom.db
```

---

## 📁 Project Structure

```bash
examples/
├── adv_checkpointing_demo.py        # 🔁 Main script with CLI interface
├── checkpoints/                     # 💾 SQLite DB stored here (default path)
```

---

## 🙌 Credits

Built with ❤️ using [LangGraph](https://github.com/langchain-ai/langgraph) and `pydantic`.

---

## 🧪 Tip

After interrupting a run, you can resume with:
```bash
python adv_checkpointing_demo.py --resume --thread-id <your_thread_id>
```
You can view history to get the right `--checkpoint-id`.

---


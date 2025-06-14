# 🤖 Day 6 - LangGraph Mini Assessment: Personality Test Bot

This bot asks the user 3 personality-related questions and classifies them as:

- **Extrovert**
- **Introvert**
- **Ambivert**

### ✅ Concepts Practiced

- Defining and updating state with a list (`answers`)
- Sequential flow with `add_edge()`
- Decision node using answer patterns
- Clean separation of logic into nodes
- Compiling and invoking graph

### 🧠 Flow

```
q1 → q2 → q3 → evaluate
```

Answers are collected and stored in `answers` list.
Based on number of "yes" vs. "no", the final personality is printed.
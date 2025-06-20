# Retry Workflows

A LangGraph implementation that creates an intelligent chatbot with automatic retry and validation capabilities.

## What This Does

This workflow asks "What is the capital of France?" and keeps retrying until it gets the correct answer containing "Paris". It demonstrates:

- 🔄 **Automatic Retry Logic** - Loops until getting correct answer
- 📊 **Answer Validation** - Grades responses as correct/incorrect/ambiguous  
- 🛡️ **Safety Limits** - Max 5 retries to prevent infinite loops
- 📝 **State Tracking** - Maintains conversation history and logs
- 💾 **Memory Persistence** - Uses checkpointer for state management

## Quick Start

### Prerequisites
```bash
pip install langgraph langchain-ollama langchain-core
```

### Run the Code
```bash
python retry_until_correct.py
```

## Code Structure

```
retry_workflows/
├── retry_until_correct.py    # Main implementation
└── README.md                 # This file
```

## Workflow Flow

```
Start → Chatbot → Grader → Router
  ↑                           ↓
  └────────← (if incorrect) ←─┘
```

1. **Start**: Initializes with the question
2. **Chatbot**: Gets LLM response using Gemma 2B
3. **Grader**: Evaluates answer quality
4. **Router**: Loops back or ends based on grade

## Configuration

### LLM Model
```python
llm = ChatOllama(model="gemma:2b", temperature=0.3)
```

### Grading Logic
- ✅ **Correct**: Contains "paris"
- ❌ **Incorrect**: Short answer (< 20 chars)  
- ⚠️ **Ambiguous**: Longer but doesn't contain "paris"

### Retry Settings
- **Max Retries**: 5 attempts
- **Thread ID**: "cap_fr"

## Sample Output

```
🚀 Starting France Capital Quiz...

--- Step ---
📝 Start node triggered

--- Step ---
📝 LLM response generated
🔄 Retry count: 1
📊 Grade: incorrect

--- Step ---
📝 Grader judged answer as incorrect

✅ Correct Answer Found!
🎯 Final Answer: The capital of France is Paris.

🏁 Quiz completed!
```

## Key Features

- **State Management**: Tracks messages, retries, logs, and grades
- **Conditional Routing**: Smart decision making based on answer quality
- **Error Prevention**: Built-in retry limits
- **Comprehensive Logging**: Step-by-step execution tracking
- **Memory Checkpointing**: Conversation state persistence

## Customization

### Change the Question
```python
def start_node(state: State) -> State:
    return {
        "messages": [HumanMessage(content="Your question here")],
        # ... rest of state
    }
```

### Modify Grading Criteria
```python
def grader_node(state: State) -> State:
    answer = messages[-1].content.lower()
    
    if "your_expected_answer" in answer:
        grade = "correct"
    # ... your custom logic
```

### Adjust Retry Limit
```python
def grade_router(state: State) -> str:
    if state["retry_count"] >= 10:  # Change from 5 to 10
        return "end"
```

## Use Cases

- ✅ Quality control for AI responses
- ✅ Educational quiz systems
- ✅ Fact verification workflows  
- ✅ Self-correcting chatbots
- ✅ Validation pipelines

## Dependencies

- `langgraph` - Workflow orchestration
- `langchain-ollama` - Local LLM integration
- `langchain-core` - Core messaging components

## License

MIT License - Feel free to use and modify!
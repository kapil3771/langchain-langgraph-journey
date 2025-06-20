# Multi-Agent Question Answering System

A simple multi-agent system that can answer questions using Wikipedia research and mathematical calculations.

## Features

- **Research Agent**: Fetches information from Wikipedia for factual questions
- **Calculator Agent**: Performs mathematical calculations and evaluations
- **Smart Routing**: Automatically determines which agent to use based on the question type
- **LLM Integration**: Uses Ollama's Gemma 2B model for final response generation

## Prerequisites

```bash
pip install langgraph langchain-ollama wikipedia-api
```

Make sure you have Ollama installed and the `gemma:2b` model downloaded:
```bash
ollama pull gemma:2b
```

## Usage

1. Save the code as `multi_agent.py`
2. Run the script:
```bash
python multi_agent.py
```
3. Enter your question when prompted

## Example Questions

**Research Questions:**
- "What is the population of Tokyo?"
- "Who is the president of France?"
- "What is the capital of Australia?"

**Math Questions:**
- "sqrt(144)"
- "2 + 3 * 4"
- "Calculate 15 * 8 - 20"

## How It Works

1. **Supervisor Node**: Entry point that routes questions to appropriate agents
2. **Research Agent**: Searches Wikipedia for factual information
3. **Calculator Agent**: Evaluates mathematical expressions safely
4. **Finalizer**: Combines results and generates a comprehensive answer using the LLM

## File Structure

```
langchain-langgraph-journey/
├── supervisor_graph.py    # Main application file
└── README.md         # This file
```

## Safety Features

- Mathematical evaluation uses a restricted environment with only safe math functions
- Wikipedia queries are handled with error catching
- No dangerous built-ins are accessible during calculation

## Customization

- Change the LLM model by modifying the `ChatOllama(model="...")` parameter
- Adjust routing logic in the `route_decision()` function
- Modify Wikipedia search parameters in `research_agent()`

## Troubleshooting

- **Ollama Connection Issues**: Make sure Ollama is running and the model is downloaded
- **Wikipedia Errors**: The system gracefully handles Wikipedia API failures
- **Math Errors**: Invalid expressions return helpful error messages

## License

Open source - feel free to modify and use as needed!
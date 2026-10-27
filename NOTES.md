# Project Notes

## Python environment

Check the installed Python version:

```bash
python3 --version
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages in the active environment:

```bash
python -m pip install openai python-dotenv requests
```

When finished, leave the virtual environment:

```bash
deactivate
```

If the virtual environment is broken, rename it before creating a fresh one:

```bash
mv .venv .venv-broken
```

## Ollama

Start the Ollama server:

```bash
ollama serve
```

In another terminal, run or list models:

```bash
ollama run qwen3:4b
ollama list
```

Stop or remove the model when needed:

```bash
ollama stop qwen3:4b
ollama rm qwen3:4b
```

## Tech stack

- **Language:** Python 3
- **Local model server:** Ollama
- **Model noted for the project:** `qwen3:4b`

> The run commands above use `qwen3:4b`; confirm which model name you intend to use.

## Interview preparation

### Why use SHA/digest names?

- A digest helps detect unexpected changes to content.
- Content-addressable storage (CAS) uses a digest as a content identifier.
- This supports integrity checks and tamper detection in distributed systems.

### Why use a `.env` file?

Keep configuration such as the API base URL and model name outside the source code. Load `.env` values with `python-dotenv` and read them with Python's `os` module instead of hard-coding them.

### Important interview questions for this project

1. What is the difference between a normal chatbot and a tool-using AI assistant?
2. Why is function calling useful in real-world AI applications?
3. How does the assistant decide when to call a tool?
4. Why do we keep model configuration in `.env` instead of in code?
5. What is the role of `TOOLS` metadata in OpenAI-compatible APIs?
6. How does `FUNCTION_NAME_TO_FUNCTION_MAP` connect LLM tool calls to Python functions?
7. Why is conversation history important for multi-turn tasks?
8. What are the limitations of this simple assistant design?
9. How would you extend this project to support more tools, memory, or a database?
10. What happens if the external weather API is slow or unavailable?

### Key project insights

- This project is a minimal example of agent-style behavior.
- The model is not magically aware of Python functions; it is guided by structured metadata.
- Tool calling is useful for tasks like retrieving real-time data, checking time, or triggering workflows.
- Simple systems like this are easy to learn and are the foundation for more advanced AI agents.

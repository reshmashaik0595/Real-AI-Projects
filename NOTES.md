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

Install the OpenAI client library in the active environment:

```bash
python -m pip install openai
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
- **Model noted for the project:** `qwen3.5:4b`

> The run commands above use `qwen3:4b`; confirm which model name you intend to use.

## Interview preparation

### Why use SHA/digest names?

- A digest can help detect unexpected changes to content.
- Content-addressable storage (CAS) uses a content's digest as its identifier.

### Why use a `.env` file?

Keep configuration such as the API base URL and model name outside the source code. Load `.env` values with `python-dotenv` and read them with Python's `os` module instead of hard-coding them.

# Examples

This directory contains example code and scripts demonstrating how to use the RAG Knowledge Assistant.

## Files

### `basic_usage.py`
Python example showing how to interact with the API using the `requests` library.

**Usage:**
```bash
python examples/basic_usage.py
```

**Features:**
- Simple query examples
- Session-based conversations
- Evaluation result inspection

### `curl_examples.sh`
Bash script with cURL examples for testing the API from the command line.

**Usage:**
```bash
./examples/curl_examples.sh
```

**Requirements:**
- `jq` (for JSON formatting): `brew install jq` or `apt-get install jq`

**Features:**
- Simple queries
- Follow-up questions
- API documentation links

### `multi_agent_example.py`
Demonstrates the multi-agent controller workflow with parallel workers, critic, and judge.

**Usage:**
```bash
python -m examples.multi_agent_example
```

**Features:**
- Multiple worker agents generating answers in parallel
- Critic agent providing feedback
- Judge agent making final decision

### `ingestion_example.py`
Shows how to ingest documents into the vector store.

**Usage:**
```bash
python -m examples.ingestion_example
```

**Features:**
- Loading documents from directory
- Creating embeddings
- Building FAISS index
- Saving for later use

## Running Examples

1. **Start the API server:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Run Python examples:**
   ```bash
   # Basic usage
   python examples/basic_usage.py
   
   # Multi-agent
   python -m examples.multi_agent_example
   
   # Ingestion
   python -m examples.ingestion_example
   ```

3. **Run shell script:**
   ```bash
   ./examples/curl_examples.sh
   ```

## Prerequisites

- API server running on `http://localhost:8000`
- Ollama running with required models (`llama3`, `nomic-embed-text`)
- Python dependencies installed (`pip install -r requirements.txt`)
- For shell script: `jq` installed for JSON formatting



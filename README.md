# RAG Knowledge Assistant

A sophisticated Retrieval-Augmented Generation (RAG) system with multi-agent architecture for intelligent question answering and knowledge retrieval.

## 🚀 Features

- **Multi-Agent Architecture**: Coordinated agents for planning, retrieval, answering, and evaluation
- **Vector Search**: FAISS-powered semantic search for efficient document retrieval
- **Session Memory**: Maintains conversational context across interactions
- **Long-Term Memory**: Persists successful Q&A interactions for future reference
- **Quality Evaluation**: Automatic answer evaluation with confidence scoring
- **Retry Logic**: Intelligent retry mechanism with escalation handling
- **RESTful API**: FastAPI-based API for easy integration
- **Ollama Integration**: Uses local LLM models (Llama3) and embeddings (nomic-embed-text)

## 📋 Table of Contents

- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Examples](#examples)
- [Contributing](#contributing)

## 🏗️ Architecture

The system follows a multi-agent orchestration pattern:

```
User Query → Planner Agent → Retriever Agent → Answer Agent → Evaluator Agent → Response
```

See [diagrams/architecture.md](diagrams/architecture.md) for detailed architecture diagrams.

### Key Components

- **Planner Agent**: Determines if retrieval is needed and how many documents to retrieve
- **Retriever Agent**: Performs semantic search using FAISS vector store
- **Answer Agent**: Generates answers using LLM with retrieved context
- **Evaluator Agent**: Assesses answer quality and confidence
- **Critic Agent**: Provides critique for multi-agent scenarios
- **Judge Agent**: Makes final decisions in multi-agent workflows
- **Worker Agents**: Specialized agents for parallel processing

## 📦 Installation

### Prerequisites

- Python 3.10+
- Ollama installed and running
- Required Ollama models:
  - `llama3` (for LLM)
  - `nomic-embed-text` (for embeddings)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rag-knowledge-assistant
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Ollama models**
   ```bash
   ollama pull llama3
   ollama pull nomic-embed-text
   ```

5. **Ingest documents** (optional)
   ```bash
   python -m app.ingestion.ingest
   ```

## 🚀 Quick Start

1. **Start Ollama** (if not already running)
   ```bash
   ollama serve
   ```

2. **Start the API server**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Test the API**
   ```bash
   curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"query": "What is RAG?", "session_id": "test-session-1"}'
   ```

4. **Access API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📚 API Documentation

### POST `/chat`

Query the knowledge assistant.

**Request Body:**
```json
{
  "query": "What is retrieval-augmented generation?",
  "session_id": "unique-session-id"
}
```

**Response:**
```json
{
  "status": "success",
  "answer": "Retrieval-Augmented Generation (RAG) is...",
  "evaluation": {
    "grounded": true,
    "confidence": 0.85
  }
}
```

**Status Codes:**
- `200`: Success
- `400`: Bad Request
- `500`: Internal Server Error

## 📁 Project Structure

```
rag-knowledge-assistant/
├── app/
│   ├── agents/          # Agent implementations
│   │   ├── planner.py
│   │   ├── retriever.py
│   │   ├── answerer.py
│   │   ├── evaluator.py
│   │   ├── critic.py
│   │   ├── judge.py
│   │   └── worker.py
│   ├── api/             # API routes
│   │   └── chat.py
│   ├── ingestion/       # Document ingestion
│   │   └── ingest.py
│   ├── memory/          # Memory management
│   │   ├── vectore_store.py
│   │   ├── session_memory.py
│   │   └── long_term_memory.py
│   ├── models/          # Pydantic models
│   │   └── Query.py
│   ├── orchestration/   # Orchestration controllers
│   │   ├── controller.py
│   │   └── multi_agent_controller.py
│   ├── rag/             # RAG pipeline
│   │   └── pipeline.py
│   ├── utils/           # Utilities
│   │   └── metrics.py
│   └── main.py          # FastAPI application
├── data/
│   └── docs/            # Documents to ingest
├── diagrams/            # Architecture diagrams
├── examples/            # Usage examples
├── requirements.txt
├── .gitignore
├── CHANGELOG.md
└── README.md
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file (optional):

```env
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=llama3
EMBEDDING_MODEL=nomic-embed-text
CONFIDENCE_THRESHOLD=0.6
MAX_RETRIES=2
```

### Model Configuration

Edit agent files to change models:
- `app/agents/planner.py`: LLM_MODEL
- `app/agents/answerer.py`: LLM_MODEL
- `app/memory/vectore_store.py`: EMBEDDING_MODEL

## 💡 Examples

See the [examples/](examples/) directory for:
- Basic API usage
- Multi-agent workflows
- Custom agent integration
- Batch processing

## 🔧 Development

### Running Tests

```bash
# Add tests when available
pytest
```

### Code Style

```bash
# Format code
black app/

# Lint code
flake8 app/
```

## 📝 License

[Add your license here]

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai/) for local LLM inference
- [FAISS](https://github.com/facebookresearch/faiss) for vector search
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework

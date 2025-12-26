# Architecture Diagrams

## System Overview

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP POST /chat
       ▼
┌─────────────────────────────────────┐
│         FastAPI Application          │
│  ┌───────────────────────────────┐  │
│  │      API Router (/chat)       │  │
│  └───────────────┬───────────────┘  │
│                  ▼                   │
│  ┌───────────────────────────────┐  │
│  │    AgentController            │  │
│  │  (Orchestration Layer)        │  │
│  └───────────────┬───────────────┘  │
└──────────────────┼──────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│         Agent Pipeline               │
│                                      │
│  ┌──────────┐    ┌──────────┐      │
│  │ Planner │───▶│Retriever │      │
│  └──────────┘    └────┬─────┘      │
│                       │             │
│  ┌──────────┐    ┌────▼─────┐      │
│  │Answerer │◀───│  Context  │      │
│  └────┬─────┘    └───────────┘      │
│       │                             │
│  ┌────▼─────┐                       │
│  │Evaluator│                       │
│  └────┬─────┘                       │
│       │                             │
│  ┌────▼─────┐                       │
│  │ Response│                       │
│  └──────────┘                       │
└──────────────────────────────────────┘
```

## Agent Flow Diagram

```
User Query
    │
    ▼
┌─────────────────┐
│  Session Memory │  ← Store user query
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Planner Agent   │  ← Decide: needs_retrieval? top_k?
└────────┬────────┘
         │
         ├─── needs_retrieval = "no" ──┐
         │                              │
         └─── needs_retrieval = "yes"  │
                   │                    │
                   ▼                    │
         ┌──────────────────┐          │
         │ Retriever Agent   │          │
         │  (FAISS Search)   │          │
         └────────┬─────────┘          │
                  │                    │
                  ▼                    │
         ┌──────────────────┐          │
         │   Context Docs    │──────────┘
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │  Answer Agent     │  ← Generate answer with LLM
         │  (Ollama/LLaMA3)  │
         └────────┬──────────┘
                  │
                  ▼
         ┌──────────────────┐
         │ Evaluator Agent  │  ← Check: grounded? confidence?
         └────────┬─────────┘
                  │
         ┌────────┴────────┐
         │                 │
    confidence ≥ 0.6   confidence < 0.6
         │                 │
         ▼                 ▼
┌──────────────┐   ┌──────────────┐
│   Success    │   │    Retry     │
│              │   │  (max 2x)    │
│ - Store in   │   └──────┬───────┘
│   session    │          │
│ - Store in   │          │
│   long-term  │          │
│ - Return     │          │
└──────────────┘          │
                          │ (after max retries)
                          ▼
                  ┌──────────────┐
                  │  Escalation  │
                  │   Handler    │
                  └──────────────┘
```

## Memory Architecture

```
┌─────────────────────────────────────┐
│         Memory System                │
│                                      │
│  ┌───────────────────────────────┐  │
│  │    Session Memory             │  │
│  │  (In-memory, per session)     │  │
│  │                               │  │
│  │  session_id:                  │  │
│  │    - [user, "query 1"]        │  │
│  │    - [assistant, "answer 1"]  │  │
│  │    - [user, "query 2"]        │  │
│  │    - ...                       │  │
│  └───────────────────────────────┘  │
│                                      │
│  ┌───────────────────────────────┐  │
│  │   Long-Term Memory            │  │
│  │  (Persistent, JSON file)      │  │
│  │                               │  │
│  │  [                              │
│  │    {                            │
│  │      "query": "...",            │
│  │      "answer": "...",           │
│  │      "evaluation": {...},       │
│  │      "retries": 0               │
│  │    },                           │
│  │    ...                          │
│  │  ]                              │
│  └───────────────────────────────┘  │
│                                      │
│  ┌───────────────────────────────┐  │
│  │   Vector Store (FAISS)        │  │
│  │  (Persistent, binary files)   │  │
│  │                               │  │
│  │  - vector_store.index          │  │
│  │  - vector_store.pkl            │  │
│  │                               │  │
│  │  Embeddings: nomic-embed-text  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

## Multi-Agent Controller Flow

```
Query + Context
    │
    ▼
┌─────────────────────────────────────┐
│    Multi-Agent Controller            │
│                                      │
│  ┌──────────┐  ┌──────────┐        │
│  │ Worker A │  │ Worker B │        │
│  │ (Expert) │  │ (Expert) │        │
│  └────┬─────┘  └────┬─────┘        │
│       │             │               │
│       └──────┬──────┘               │
│              │                      │
│       ┌──────▼──────┐               │
│       │ Worker C    │               │
│       │ (Expert)   │               │
│       └──────┬─────┘               │
│              │                      │
│       ┌──────▼──────┐               │
│       │  Answers    │               │
│       │  [A, B, C]  │               │
│       └──────┬──────┘               │
│              │                      │
│       ┌──────▼──────┐               │
│       │  Critic     │               │
│       │  Agent      │               │
│       └──────┬──────┘               │
│              │                      │
│       ┌──────▼──────┐               │
│       │   Judge     │               │
│       │   Agent     │               │
│       └──────┬──────┘               │
│              │                      │
│       ┌──────▼──────┐               │
│       │Final Answer │               │
│       └─────────────┘               │
└─────────────────────────────────────┘
```

## Data Flow

```
Document Ingestion
    │
    ▼
┌─────────────────┐
│  Load Documents │  (from data/docs/)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Embed Text     │  (nomic-embed-text via Ollama)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Add to FAISS   │  (vector_store.index)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Save Index     │  (vector_store.pkl for metadata)
└─────────────────┘

Query Processing
    │
    ▼
┌─────────────────┐
│  Embed Query    │  (nomic-embed-text)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FAISS Search   │  (find top-k similar vectors)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Retrieve Docs  │  (map indices to text)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Build Prompt   │  (context + query)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LLM Generate   │  (llama3 via Ollama)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Return Answer  │
└─────────────────┘
```

## Component Interaction

```
┌──────────────┐
│   Ollama     │
│   Service    │
│              │
│  - llama3    │
│  - nomic-    │
│    embed-    │
│    text      │
└──────┬───────┘
       │
       │ HTTP API
       │
       ▼
┌─────────────────────────────────────┐
│      RAG Knowledge Assistant         │
│                                      │
│  ┌────────────┐  ┌──────────────┐  │
│  │   Agents   │  │   Memory     │  │
│  │            │  │              │  │
│  │ - Planner  │  │ - Session    │  │
│  │ - Retriever│  │ - Long-term  │  │
│  │ - Answerer │  │ - Vector     │  │
│  │ - Evaluator│  │   Store      │  │
│  └────────────┘  └──────────────┘  │
│                                      │
│  ┌──────────────────────────────┐   │
│  │      FastAPI Server          │   │
│  │   (Port 8000)                │   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
       │
       │ HTTP REST API
       │
       ▼
┌──────────────┐
│   Clients    │
│              │
│  - Web Apps  │
│  - CLI Tools │
│  - Services  │
└──────────────┘
```


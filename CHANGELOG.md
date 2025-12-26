# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Multi-agent orchestration system
- Session memory for conversational context
- Long-term memory for persistent Q&A storage
- Answer evaluation with confidence scoring
- Retry logic with escalation handling
- FAISS vector store integration
- FastAPI REST API
- Ollama integration for local LLM inference
- Document ingestion pipeline
- Metrics tracking system

### Changed
- Improved error handling in vector store operations
- Enhanced API response structure

### Fixed
- Fixed dimension mismatch in FAISS index loading
- Fixed JSON parsing for streaming Ollama responses
- Fixed module import paths for proper package structure

## [0.1.0] - 2024-01-XX

### Added
- Initial release
- Basic RAG pipeline
- Vector store with FAISS
- Simple API endpoint
- Document ingestion script

[Unreleased]: https://github.com/yourusername/rag-knowledge-assistant/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/rag-knowledge-assistant/releases/tag/v0.1.0


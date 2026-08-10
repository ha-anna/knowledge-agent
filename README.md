# Knowledge Agent

An AI-powered knowledge assistant that lets users upload their own documents and ask questions using Retrieval-Augmented Generation (RAG).

Built to explore modern AI backend engineering with FastAPI, local LLMs, and vector search.

## Why I Built This

Large Language Models are powerful, but they don't know anything about your own documents.

This project explores how Retrieval-Augmented Generation (RAG) can be used to build domain-specific AI assistants that answer questions using uploaded PDFs and other knowledge sources.

The goal is to understand the architecture behind production AI systems rather than simply calling an LLM API.

## Knowledge Agent — Project Progress

### Backend

- [x] FastAPI backend
- [x] Project structure
- [x] Configuration & environment variables
- [x] Dependency injection
- [x] Logging

### Documents

- [x] PDF upload
- [x] File storage
- [x] Text extraction
- [x] Document metadata
- [x] List / Get / Delete documents

### Document Processing

- [x] Document chunking
- [x] Embedding generation
- [x] Vector database
- [x] Store embeddings & metadata

### Retrieval

- [x] Vector search
- [x] Reranking
- [ ] Retrieval quality improvements

### LLM

- [x] Local LLM integration
- [x] Ollama + Docker
- [x] LLM service
- [ ] Streaming responses
- [ ] Error handling

### RAG

- [x] Context retrieval
- [x] Context construction
- [x] RAG prompt
- [x] Grounded answers
- [ ] Source citations
- [ ] Improve grounding / retrieval quality

### Conversations

- [x] Conversation creation
- [x] Message storage
- [x] Conversation history
- [x] Multi-turn conversations
- [ ] Persistent conversation storage
- [ ] Conversation management

### Agent

- [ ] RAG vs. normal conversation
- [ ] Follow-up questions
- [ ] Better use of conversation context

### API & Quality

- [x] Document endpoints
- [x] Conversation endpoints
- [ ] Better error handling
- [ ] Automated tests
- [ ] API polish

### Deployment

- [x] Docker development environment
- [x] Docker Compose
- [x] Ollama container
- [ ] Production deployment

## Tech Stack

### Backend

- FastAPI

### AI

- Ollama
- Sentence Transformers

### Vector Database

- ChromaDB

### Database

- SQLite (initially)

### Development

- Docker
- VS Code Dev Containers
- pip-tools

## Learning Goals

This project is intentionally being built from scratch to learn:

- API design with FastAPI
- Modern Python backend development
- Retrieval-Augmented Generation
- Vector databases
- Embeddings
- AI agent architecture
- Docker workflows
- Production-oriented project structure


## Roadmap

### Phase 1

- FastAPI
- File uploads
- PDF parsing
- Basic RAG

### Phase 2

- Knowledge bases
- Search
- Chat history

### Phase 3

- AI features
- Summaries
- Flashcards

### Phase 4

- Tool-using AI agent


## Project Status

🚧 Under active development

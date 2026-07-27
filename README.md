# Knowledge Agent

An AI-powered knowledge assistant that lets users upload their own documents and ask questions using Retrieval-Augmented Generation (RAG).

Built to explore modern AI backend engineering with FastAPI, local LLMs, and vector search.

## Why I Built This

Large Language Models are powerful, but they don't know anything about your own documents.

This project explores how Retrieval-Augmented Generation (RAG) can be used to build domain-specific AI assistants that answer questions using uploaded PDFs and other knowledge sources.

The goal is to understand the architecture behind production AI systems rather than simply calling an LLM API.

## Features

- [x] FastAPI backend
- [x] Project structure
- [x] PDF upload
- [x] Save files
- [x] Text extraction
- [x] Save metadata
- [x] List/Get/Delete documents
- [ ] Document chunking
- [ ] Embedding generation
- [ ] Vector search
- [ ] Local LLM integration
- [ ] Retrieval-Augmented Generation
- [ ] Source citations
- [ ] Conversation history

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

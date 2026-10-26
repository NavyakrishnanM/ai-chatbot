# DevAssist — AI Developer Knowledge Assistant

An AI-powered chatbot that lets developers upload technical documents and ask questions about them using RAG (Retrieval-Augmented Generation) and AI agents.

## Architecture

```
Angular Frontend  →  Spring Boot Backend  →  Python FastAPI AI Service
                                                    ↓              ↓
                                               LLM Provider    PostgreSQL + pgvector
```

## Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Frontend   | Angular 18+, TypeScript, Signals  |
| Backend    | Java 21, Spring Boot, Maven       |
| AI Service | Python, FastAPI, Pydantic         |
| Database   | PostgreSQL + pgvector             |
| AI         | LLM (configurable), Embeddings    |

## Getting Started

See `docs/setup.md` for full setup instructions.

## Project Phases

- [x] Phase 1: Project Foundation
- [ ] Phase 2: Basic Chatbot
- [ ] Phase 3: Document Upload
- [ ] Phase 4: RAG Implementation
- [ ] Phase 5: Agentic AI
- [ ] Phase 6: Multi-Agent Workflow
- [ ] Phase 7: Production Features

## Learning Notes

See `docs/learning-notes.md` for concepts learned at each phase.

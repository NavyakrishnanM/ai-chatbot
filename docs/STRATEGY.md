# DevAssist — Project Strategy & Learning Roadmap

> **Role**: Senior Full-Stack Engineer + AI Engineer + Personal Mentor  
> **Goal**: Help you independently build, understand, and explain a full-stack RAG + Agentic AI application.

---

## 1. Who This Document Is For

You are a developer who knows **Angular, TypeScript, HTML/CSS**, is learning **Java/Spring Boot**, and is a **beginner in LLMs, RAG, embeddings, and AI agents**. This document is your single source of truth for what we are building, why, and in what order.

---

## 2. What We Are Building

**DevAssist** — an AI-powered developer assistant that:
- Lets users upload technical documents (PDF, TXT, Markdown)
- Asks questions about them in a chat interface
- Retrieves relevant sections from those documents (RAG)
- Generates grounded, cited answers using an LLM
- Eventually uses AI agents to handle complex queries (tool calling, multi-step reasoning)

### Example Use Cases
| User Question | What DevAssist Does |
|---|---|
| "Explain the authentication flow" | Finds the auth section in uploaded docs, summarises it |
| "What does this API endpoint do?" | Retrieves the API spec chunk, answers with the source |
| "Explain this Spring Boot error" | Uses an agent tool to look up error explanations |
| "Summarise this document" | Retrieves top chunks, generates a summary with citations |

---

## 3. Architecture

```
+-------------------------------------------------------------+
|                     User (Browser)                          |
+---------------------------+---------------------------------+
                            | HTTP (JSON)
                            v
+-------------------------------------------------------------+
|            Angular Frontend  (port 4200)                    |
|  * Chat UI, message input, history, document upload         |
|  * Standalone components, Signals, HttpClient               |
+---------------------------+---------------------------------+
                            | REST API  (JSON)
                            v
+-------------------------------------------------------------+
|          Spring Boot Backend  (port 8080)                   |
|  * Auth (JWT), chat sessions, document metadata             |
|  * Validates requests, enforces access control              |
|  * Proxies AI requests to Python service                    |
+---------------------------+---------------------------------+
                            | HTTP (JSON / multipart)
                            v
+-------------------------------------------------------------+
|          Python FastAPI AI Service  (port 8000)             |
|  * LLM calls (Gemini / OpenAI)                              |
|  * Document processing (PDF, TXT, MD)                       |
|  * Chunking, embeddings, vector storage                     |
|  * RAG retrieval pipeline                                   |
|  * Agent + tool orchestration                               |
+--------------+------------------------------+---------------+
               |                              |
               v                              v
    +------------------+          +------------------------+
    |   LLM Provider   |          |  PostgreSQL + pgvector  |
    | (Gemini / OpenAI)|          |  (chat history, docs,   |
    +------------------+          |   embeddings)           |
                                  +------------------------+
```

### Why This Separation?

| Service | Responsibility | Why Separate? |
|---|---|---|
| Angular | UI only: render, capture input, display | Frontend can evolve without touching backend |
| Spring Boot | Auth, business logic, data, sessions | Java ecosystem excels at enterprise security + DB |
| Python | AI/ML: LLMs, embeddings, RAG | Python has the best AI library ecosystem |

---

## 4. Technology Stack

| Layer | Technology | Why |
|---|---|---|
| Frontend | Angular 18+, TypeScript, Signals, RxJS | You already know it; modern reactive patterns |
| Backend | Java 21, Spring Boot, Maven, Spring Security | Industry standard for enterprise APIs |
| AI Service | Python 3.11+, FastAPI, Pydantic | Best AI/ML ecosystem; FastAPI is modern + fast |
| Database | PostgreSQL 15+ + pgvector | One DB for relational data AND vector embeddings |
| LLM | Google Gemini (free tier) or OpenAI | Configurable via environment variable |
| Auth | JWT (JSON Web Tokens) | Stateless, industry standard |

---

## 5. Development Phases

### Phase 1 — Project Foundation (COMPLETE)
- [x] Architecture explained
- [x] Folder structure created
- [x] Environment variables configured
- [x] .env.example committed
- [x] Health-check endpoints planned

### Phase 2 — Basic Chatbot (CURRENT)
**Goal**: A working end-to-end chat flow. User types a message -> Angular -> Spring Boot -> Python -> LLM -> answer displayed.

**What you will learn:**
- How HTTP requests flow between three services
- What an LLM API call looks like
- Prompts, tokens, temperature
- Loading states, error handling in Angular
- REST API design in Spring Boot
- Python async HTTP calls to an LLM

**Deliverables:**
- [ ] Angular chat UI (message list, input box, send button)
- [ ] Angular ChatService calling Spring Boot
- [ ] Spring Boot /api/chat endpoint
- [ ] Spring Boot calling Python /chat
- [ ] Python calling Gemini/OpenAI API
- [ ] End-to-end message flow working

### Phase 3 — Document Upload (PENDING)
- Angular file upload UI
- Spring Boot multipart endpoint + metadata in DB
- Python document processing (PDF/TXT/MD extraction)

### Phase 4 — RAG Pipeline (PENDING)
- Text chunking strategy
- Embeddings generation
- pgvector storage
- Semantic similarity search
- Context construction + grounded answers with citations

### Phase 5 — Agentic AI / Single Agent (PENDING)
- Agent vs chatbot distinction
- Tool calling: search_documents, search_chat_history, explain_error, retrieve_api_docs
- Tool selection, argument generation, execution, result injection

### Phase 6 — Multi-Agent Workflow (PENDING)
- Knowledge Agent, Code Assistant Agent, Planner Agent, Coordinator Agent
- When multiple agents help vs. one agent with tools

### Phase 7 — Production Features (PENDING)
- JWT authentication, user-specific sessions
- Document access control per user
- Rate limiting, retries, timeouts
- Logging, validation, error handling
- Prompt injection protection
- Basic RAG evaluation

---

## 6. Teaching Rules (How We Work)

1. **Explain before code** — every concept gets a plain-English explanation first
2. **Small tasks** — you implement; I review; we fix together
3. **No black boxes** — every file's responsibility is explained before it is created
4. **Errors are lessons** — when something breaks, we debug together step by step
5. **No phase complete** unless you confirm you understand AND have implemented it

---

## 7. Learning Checkpoints (End of Each Phase)

At the end of each phase:
- Summary of what was learned
- 3 beginner concept questions
- 2 practical interview questions
- 1 implementation challenge

---

## 8. Key Learning Goals (Interview-Ready)

By the end of this project you should be able to explain:
- [ ] Why we use microservices and how they communicate
- [ ] What RAG is and why it reduces hallucinations
- [ ] What embeddings are and how semantic search works
- [ ] What chunking is and why chunk size matters
- [ ] What an AI agent is vs. a simple chatbot
- [ ] What tool calling is and how an LLM decides which tool to use
- [ ] How JWT authentication works
- [ ] How prompt injection attacks work and how to prevent them

---

## 9. Git Commit Convention

Format:
  feat(phase): short description
  fix(service): what was broken and what was fixed
  docs: what was updated

Examples:
  feat(frontend): add chat UI with message list and input box
  feat(backend): add /api/chat endpoint with Spring Boot
  feat(ai): integrate Gemini API for basic chat response

---

## 10. Current Status

| Phase | Status | Notes |
|---|---|---|
| Phase 1 | COMPLETE | Foundation created |
| Phase 2 | IN PROGRESS | Starting Angular chat UI |
| Phase 3-7 | PENDING | - |

---

## 11. First Milestone (Most Important)

> Build a chatbot that accepts a question, retrieves relevant information from one uploaded PDF, and answers with citations.

Once that works, we add tools and agents.

---

*Last updated: Phase 2 start*

# Learning Notes — DevAssist

A personal journal of concepts learned while building DevAssist.

---

## Phase 1: Project Foundation

### What I Learned
- [ ] Why we separate Angular, Spring Boot, and Python into different services
- [ ] How services communicate over HTTP
- [ ] What a health-check endpoint is and why it matters
- [ ] What environment variables are and why we never hardcode secrets
- [ ] Git basics — .gitignore, commits

### Key Concepts

**Microservices**: Splitting an application into separate services where each service does one thing well.
- Angular = UI only
- Spring Boot = business logic + auth + database
- Python = AI processing

**Environment Variables**: Configuration values stored outside code, so secrets are never committed to Git.

**Health Check**: A simple `/health` endpoint that returns `{ "status": "UP" }`. Used to verify a service is running.

---

## Phase 2: Basic Chatbot

*(Coming soon)*

---

## Phase 3: Document Upload

*(Coming soon)*

---

## Phase 4: RAG

*(Coming soon)*

---

## Phase 5: Agentic AI

*(Coming soon)*

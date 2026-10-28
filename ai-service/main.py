# ============================================================
# main.py  —  FastAPI Application Entry Point
# ============================================================
# PURPOSE: Creates the FastAPI app, registers all routers,
#          configures CORS, and starts the server.
#
# ANALOGY to Spring Boot:
#   This file is like your @SpringBootApplication class.
#   It's where everything is wired together and the server starts.
#
# CONCEPT — CORS (Cross-Origin Resource Sharing):
#   By default, browsers BLOCK requests from one origin (e.g.
#   localhost:4200) to another (localhost:8000). CORS is a
#   mechanism that tells the browser "it's okay, I allow it".
#   Without CORS configured, Angular can't talk to this service.
#   In Phase 2, we'll allow all origins for development.
#   In Phase 7 (production), we'll lock this down to specific URLs.
# ============================================================

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Import our routers — each router is a group of related endpoints
from routers.chat import router as chat_router

# Load .env file before anything else reads environment variables
load_dotenv()

# ============================================================
# Logging Setup
# ============================================================
# logging is Python's built-in logging library.
# INFO level means we see: info, warnings, and errors.
# DEBUG level would also show detailed trace logs.
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


# ============================================================
# Lifespan — Startup / Shutdown Logic
# ============================================================
# Modern FastAPI uses a "lifespan" context manager instead of
# @app.on_event("startup"). It's cleaner: everything before
# "yield" runs at startup, everything after runs at shutdown.
#
# ANALOGY: Like @PostConstruct / @PreDestroy in Spring Boot.
# ============================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP ---
    provider = os.getenv("LLM_PROVIDER", "gemini")
    logger.info("DevAssist AI Service starting up...")
    logger.info(f"LLM Provider: {provider}")

    if provider == "gemini":
        key = os.getenv("GEMINI_API_KEY", "")
        if not key or key == "your_gemini_api_key_here":
            logger.warning(
                "GEMINI_API_KEY is not set! "
                "Update the .env file with your key from https://aistudio.google.com"
            )
        else:
            logger.info("Gemini API key found. Ready to handle requests.")

    logger.info("Swagger docs available at: http://localhost:8000/docs")

    yield  # <-- server is running and handling requests here

    # --- SHUTDOWN ---
    logger.info("DevAssist AI Service shutting down.")


# ============================================================
# Create the FastAPI Application
# ============================================================
# FastAPI() is like creating the Spring Boot application context.
# The title and description appear in the auto-generated docs
# at http://localhost:8000/docs  ← you can test all endpoints here!
# ============================================================
app = FastAPI(
    title="DevAssist AI Service",
    description="Python FastAPI service handling LLM calls, RAG, and AI agents for DevAssist.",
    version="0.1.0",
    docs_url="/docs",      # Swagger UI — interactive API docs
    redoc_url="/redoc",    # ReDoc — alternative API docs
    lifespan=lifespan      # Register the startup/shutdown handler
)


# ============================================================
# CORS Middleware
# ============================================================
# allow_origins: which frontends are allowed to call us
#   ["*"] = allow everyone (development only — tighten in prod)
# allow_methods: which HTTP methods are allowed
# allow_headers: which headers are allowed (e.g. Content-Type)
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # TODO Phase 7: restrict to ["http://localhost:4200"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Register Routers
# ============================================================
# prefix="/chat" + the router's own prefix="/chat" → /chat/...
# We use a top-level /api prefix so all our routes are at:
#   POST /api/chat
#   GET  /api/chat/health
# Spring Boot will call these URLs.
# ============================================================
app.include_router(chat_router, prefix="/api")


# ============================================================
# Root Health Check
# ============================================================
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Top-level health check.
    Spring Boot and monitoring tools call this to verify service is UP.
    Returns: { "status": "UP", "service": "devassist-ai-service" }
    """
    provider = os.getenv("LLM_PROVIDER", "gemini")
    return {
        "status": "UP",
        "service": "devassist-ai-service",
        "llm_provider": provider,
        "version": "0.1.0"
    }


# ============================================================
# Run with Uvicorn (for direct python main.py execution)
# ============================================================
# Normally you run: uvicorn main:app --reload
# But this block lets you also run: python main.py
# "reload=True" means the server restarts automatically when
# you change a file — very useful during development.
# ============================================================
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("AI_SERVICE_PORT", "8000"))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,     # auto-restart on file changes
        log_level="info"
    )

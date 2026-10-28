# ============================================================
# routers/chat.py
# ============================================================
# PURPOSE: Defines the HTTP endpoints for chat.
#
# In Spring Boot, this is your @RestController.
# In FastAPI, we use APIRouter — a group of related endpoints
# that we can "include" in the main app cleanly.
#
# This file ONLY handles:
#   - Receiving the HTTP request
#   - Validating the input (FastAPI does this automatically)
#   - Calling the service layer (llm_service)
#   - Returning the HTTP response
#
# It does NOT contain any business logic or LLM code.
# That's the job of services/llm_service.py.
# This separation makes code easier to test and maintain.
# ============================================================

from fastapi import APIRouter, HTTPException
from models.chat_models import ChatRequest, ChatResponse
from services.llm_service import generate_response
import logging

# Logger — we log what's happening so we can debug issues
logger = logging.getLogger(__name__)

# APIRouter groups related endpoints together
# prefix="/chat" means all routes here start with /chat
router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post(
    "",                        # Full path will be: POST /chat
    response_model=ChatResponse,  # FastAPI validates our return against this model
    summary="Send a message and get an AI response"
)
async def send_message(request: ChatRequest):
    """
    Receives a chat message from Spring Boot and returns an AI response.

    Flow:
    1. FastAPI validates the incoming JSON against ChatRequest
    2. We call llm_service.generate_response() with the user's message
    3. We return a ChatResponse (FastAPI serialises it to JSON)

    If anything goes wrong, we raise an HTTPException with a
    meaningful error message — this becomes a proper HTTP error
    response (400, 500, etc.) instead of a crash.
    """
    logger.info(f"Received chat request. Session: {request.session_id}")

    try:
        # Delegate to the service layer — the router doesn't talk
        # to Gemini directly, that's llm_service's job
        result = await generate_response(request.message)

        logger.info(f"LLM responded using model: {result['model_used']}")

        # Build and return the response object
        # FastAPI will convert this to JSON automatically
        return ChatResponse(
            reply=result["reply"],
            session_id=request.session_id,
            model_used=result["model_used"]
        )

    except ValueError as e:
        # ValueError means configuration is wrong (e.g. missing API key)
        # 400 Bad Request — something is wrong with our setup
        logger.error(f"Configuration error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Catch-all for unexpected errors
        # 503 Service Unavailable — the LLM call failed
        logger.error(f"LLM call failed: {e}")
        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable. Please try again."
        )


@router.get("/health", summary="Health check for the chat router")
async def chat_health():
    """
    Simple health check so Spring Boot can verify this route works.
    Returns 200 OK with a status message.
    """
    return {"status": "UP", "service": "chat-router"}

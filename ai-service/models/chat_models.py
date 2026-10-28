# ============================================================
# models/chat_models.py
# ============================================================
# PURPOSE: Defines the shape of data coming IN and going OUT.
#
# In Spring Boot you would use DTOs (Data Transfer Objects).
# In Python/FastAPI we use Pydantic models — they do the same
# job: define fields, types, and validations.
#
# FastAPI automatically validates incoming JSON against these
# models and returns a 422 error if the data is wrong shape.
# ============================================================

from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    """
    What Angular / Spring Boot sends us when a user types a message.

    Example JSON:
    {
        "message": "What is dependency injection?",
        "session_id": "abc-123"
    }
    """
    message: str = Field(
        ...,                          # "..." means required — cannot be empty
        min_length=1,                 # message must have at least 1 character
        max_length=4000,              # guard against huge inputs
        description="The user's question or message"
    )
    session_id: Optional[str] = Field(
        default=None,
        description="Chat session ID — used later to maintain conversation history"
    )


class ChatResponse(BaseModel):
    """
    What we send back after the LLM responds.

    Example JSON:
    {
        "reply": "Dependency injection is a design pattern where...",
        "session_id": "abc-123",
        "model_used": "gemini-1.5-flash"
    }
    """
    reply: str = Field(description="The AI's answer to the user's question")
    session_id: Optional[str] = Field(default=None)
    model_used: str = Field(description="Which LLM model generated this response")

# ============================================================
# services/llm_service.py
# ============================================================
# PURPOSE: All LLM communication lives here.
#
# This is the "AI brain" of our service. It:
#   1. Reads which LLM provider to use from .env
#   2. Builds a system prompt (instructions for the AI)
#   3. Calls the LLM API with the user's message
#   4. Returns the plain text reply
#
# CONCEPT — System Prompt vs User Message:
#   Imagine you hired an employee. Before they start answering
#   calls, you give them a training manual (system prompt).
#   Every customer call (user message) is then answered using
#   that training. The LLM works the same way.
#
# CONCEPT — Why async/await?
#   When Python calls an external API (like Gemini), it has to
#   WAIT for the network response. Using async/await lets the
#   server handle other requests while waiting, instead of
#   sitting idle. This is like a waiter taking multiple orders
#   instead of standing at one table the whole time.
#
# SDK NOTE:
#   We use the NEW google-genai SDK (google.genai).
#   The old google-generativeai package is deprecated.
#   The new SDK has a cleaner, client-based API.
# ============================================================

import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from the .env file into os.environ
# This must be called before we read any env variables
load_dotenv()


# ============================================================
# SYSTEM PROMPT
# ============================================================
# This is the "training manual" we give the LLM before every
# conversation. It tells the AI:
#   - Who it is
#   - What it should do
#   - How it should behave
#   - What it should NOT do
#
# Good system prompts are critical in production. They prevent
# the AI from going off-topic, making things up, or being rude.
# ============================================================
SYSTEM_PROMPT = """You are DevAssist, an AI assistant that helps software developers.

Your role:
- Answer questions about programming, software architecture, APIs, and technical concepts
- Explain errors and how to fix them
- When you don't know something, say so clearly instead of guessing
- Keep answers concise and practical
- Use code examples when helpful

You are currently in basic chat mode (no documents uploaded yet).
In future phases, you will be able to search uploaded documents and cite them.

Tone: Professional, clear, and encouraging to learners."""


def get_llm_provider() -> str:
    """
    Reads LLM_PROVIDER from .env and returns it.
    Defaults to 'gemini' if not set.
    """
    return os.getenv("LLM_PROVIDER", "gemini").lower()


async def call_gemini(user_message: str) -> dict:
    """
    Calls the Google Gemini API using the new google-genai SDK.

    Parameters:
        user_message: The question the user typed in Angular

    Returns:
        A dict with 'reply' (the AI's answer) and 'model_used'

    CONCEPT — async vs sync SDK calls:
        The Gemini SDK has two versions of each method:
          - generate_content()        → synchronous (BLOCKS the event loop)
          - generate_content_async()  → async (NON-BLOCKING, correct for FastAPI)

        Using the sync version inside an async function causes the entire
        server to freeze while waiting for the API — no other requests can
        be handled. Always use the async version in FastAPI.
        This is like the difference between a blocking DB query vs a
        non-blocking async query in Spring WebFlux.
    """

    # Read the API key from environment — never hardcode this!
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        raise ValueError(
            "GEMINI_API_KEY is not set in your .env file. "
            "Get a free key at https://aistudio.google.com"
        )

    # Create the Gemini client — this is the entry point for all API calls
    client = genai.Client(api_key=api_key)

    # Choose the model — use a stable alias rather than a pinned version
    # Aliases like "gemini-flash-lite-latest" always point to a working
    # model, unlike pinned names (e.g. "gemini-3.8-flash") which can be
    # retired or overloaded on the free tier.
    # Swap to "models/gemini-flash-latest" or "models/gemini-pro-latest"
    # for higher quality when needed.
    model_name = "models/gemini-flash-lite-latest"

    # Use generate_content_async — the non-blocking async version
    # GenerateContentConfig passes optional settings:
    #   system_instruction → our "training manual" for the AI
    #   temperature        → how creative (0 = factual, 1 = creative)
    #   max_output_tokens  → caps response length
    response = await client.aio.models.generate_content(
        model=model_name,
        contents=user_message,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.7,
            max_output_tokens=1024,
        )
    )

    # response.text is the plain text answer from Gemini
    return {
        "reply": response.text,
        "model_used": model_name
    }


async def generate_response(user_message: str) -> dict:
    """
    Main entry point called by the router.
    Routes to the correct LLM based on LLM_PROVIDER in .env.

    This pattern means we can swap LLM providers without changing
    any other file — just update the .env variable.
    """
    provider = get_llm_provider()

    if provider == "gemini":
        return await call_gemini(user_message)
    else:
        # We'll add OpenAI support in a later lesson
        raise NotImplementedError(
            f"LLM provider '{provider}' is not supported yet. "
            "Set LLM_PROVIDER=gemini in your .env file."
        )

package com.devassist.dto;

/**
 * ChatResponse DTO
 *
 * This is what Spring Boot sends back to Angular after getting
 * the AI's answer from the Python service.
 *
 * Jackson will serialize this record to JSON automatically:
 *   new ChatResponse("Dependency injection is...", "gemini-flash-lite-latest")
 *   → {"reply": "Dependency injection is...", "modelUsed": "gemini-flash-lite-latest"}
 *
 * Note: Jackson converts camelCase field names to camelCase JSON keys.
 * modelUsed (Java) → "modelUsed" (JSON) — Angular reads it as response.modelUsed
 */
public record ChatResponse(
        String reply,
        String modelUsed
) {}


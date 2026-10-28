package com.devassist.service;

import com.devassist.dto.ChatRequest;
import com.devassist.dto.ChatResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientException;

import java.util.Map;

/**
 * ChatService — Business Logic Layer
 *
 * CONCEPT — @Service:
 * Marks this class as a Spring-managed "service bean". Spring creates
 * one instance (singleton) and injects it wherever it's needed via
 * @Autowired or constructor injection. You never call "new ChatService()"
 * yourself — Spring handles the lifecycle.
 *
 * CONCEPT — Separation of Concerns:
 *   Controller  → knows about HTTP (request/response, status codes)
 *   Service     → knows about business logic (how to get the AI answer)
 *   (Future) Repository → knows about the database
 *
 * The controller doesn't know or care HOW we get the AI answer.
 * It just calls chatService.chat(request) and returns the result.
 * This makes each layer independently testable and replaceable.
 *
 * CONCEPT — RestClient (Spring 6.1+):
 * RestClient is the modern fluent HTTP client in Spring Boot 3.2+.
 * It replaces the older RestTemplate (which still works but is legacy).
 * We use it here to call our Python FastAPI service as an HTTP client.
 *
 * Think of RestClient like Angular's HttpClient — it makes HTTP requests
 * from Java code to other services.
 */
@Service
public class ChatService {

    private static final Logger log = LoggerFactory.getLogger(ChatService.class);

    // RestClient is the HTTP client we'll use to call Python
    private final RestClient restClient;

    /**
     * CONCEPT — @Value:
     * Reads a value from application.properties (or environment variables).
     * "${ai.service.url}" maps to the key "ai.service.url" in properties.
     * This is how we avoid hardcoding URLs — change the property, not the code.
     *
     * CONCEPT — Constructor Injection (preferred over @Autowired on fields):
     * Spring sees this constructor, finds a RestClient.Builder bean
     * (auto-configured by Spring Boot), and injects it automatically.
     * Constructor injection is preferred because:
     *   - Fields are final (immutable after construction)
     *   - Easier to test (pass mocks via constructor)
     *   - Fails fast at startup if a dependency is missing
     */
    public ChatService(
            RestClient.Builder restClientBuilder,
            @Value("${ai.service.url}") String aiServiceUrl
    ) {
        this.restClient = restClientBuilder
                .baseUrl(aiServiceUrl)  // e.g. http://localhost:8000
                .build();
    }

    /**
     * Sends the user's message to the Python AI service and returns the response.
     *
     * CONCEPT — Request/Response Flow:
     * 1. Angular  →  POST /api/chat  {"message": "..."}  → Spring Boot
     * 2. Spring Boot (this method) → POST /api/chat {"message": "..."} → Python
     * 3. Python → Gemini → answer
     * 4. Python → {"reply": "...", "model_used": "..."} → Spring Boot
     * 5. Spring Boot → {"reply": "...", "modelUsed": "..."} → Angular
     *
     * @param request The validated ChatRequest from the controller
     * @return ChatResponse containing the AI's reply
     */
    public ChatResponse chat(ChatRequest request) {
        log.info("Forwarding chat request to AI service. Message length: {} chars",
                request.message().length());

        try {
            // Build the payload map to send to Python
            // Python expects: {"message": "..."}
            Map<String, String> pythonPayload = Map.of("message", request.message());

            // CONCEPT — RestClient fluent API:
            // .post()               → HTTP POST method
            // .uri("/api/chat")     → appended to baseUrl
            // .body(pythonPayload)  → Jackson serializes the Map to JSON
            // .retrieve()           → send the request
            // .body(Map.class)      → deserialize the JSON response body

            @SuppressWarnings("unchecked")
            Map<String, Object> pythonResponse = restClient
                    .post()
                    .uri("/api/chat")
                    .body(pythonPayload)
                    .retrieve()
                    .body(Map.class);

            if (pythonResponse == null) {
                throw new RuntimeException("Empty response received from AI service");
            }

            String reply = (String) pythonResponse.getOrDefault("reply", "No reply received");
            String modelUsed = (String) pythonResponse.getOrDefault("model_used", "unknown");

            log.info("Received response from AI service. Model: {}", modelUsed);

            return new ChatResponse(reply, modelUsed);

        } catch (RestClientException e) {
            // RestClientException covers connection errors, timeouts, 4xx/5xx from Python
            log.error("Failed to reach AI service: {}", e.getMessage());
            throw new RuntimeException(
                    "AI service is currently unavailable. Please try again shortly.", e
            );
        }
    }
}


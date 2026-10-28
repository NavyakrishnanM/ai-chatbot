package com.devassist.controller;

import com.devassist.dto.ChatRequest;
import com.devassist.dto.ChatResponse;
import com.devassist.service.ChatService;
import jakarta.validation.Valid;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * ChatController — HTTP Layer
 *
 * CONCEPT — @RestController:
 * Combines @Controller + @ResponseBody.
 * Every method return value is automatically serialized to JSON.
 * Without @ResponseBody, Spring would try to find an HTML template
 * with that name — not what we want for a REST API.
 *
 * CONCEPT — @RequestMapping("/api/chat"):
 * All endpoints in this controller are prefixed with /api/chat.
 * This is the base path; individual methods add more specifics.
 *
 * CONCEPT — Controller's ONLY job:
 * 1. Receive the HTTP request
 * 2. Validate the input (@Valid)
 * 3. Call the service
 * 4. Return the HTTP response with the right status code
 *
 * The controller does NOT contain business logic. It delegates
 * everything to ChatService. This keeps it thin and focused.
 */
@RestController
@RequestMapping("/api/chat")
public class ChatController {

    private static final Logger log = LoggerFactory.getLogger(ChatController.class);

    // Injected by Spring via constructor injection
    private final ChatService chatService;

    public ChatController(ChatService chatService) {
        this.chatService = chatService;
    }

    /**
     * POST /api/chat
     * Accepts a user message and returns an AI-generated response.
     *
     * CONCEPT — @PostMapping:
     * Maps HTTP POST requests to this method. GET is for fetching data,
     * POST is for sending data that triggers an action (like an LLM call).
     *
     * CONCEPT — @RequestBody:
     * Tells Spring to read the HTTP request body (JSON) and deserialize
     * it into a ChatRequest object. Jackson handles the JSON → Java mapping.
     *
     * CONCEPT — @Valid:
     * Triggers Bean Validation on the ChatRequest.
     * If @NotBlank or @Size fails, Spring automatically returns:
     *   HTTP 400 Bad Request with a validation error message.
     * You don't write that error handling yourself.
     *
     * CONCEPT — ResponseEntity<T>:
     * Lets you control the HTTP status code explicitly.
     * ResponseEntity.ok(body) → HTTP 200 OK + JSON body
     * This is more explicit than just returning the object directly.
     */
    @PostMapping
    public ResponseEntity<ChatResponse> chat(@Valid @RequestBody ChatRequest request) {
        log.info("POST /api/chat received");

        ChatResponse response = chatService.chat(request);

        return ResponseEntity.ok(response);
    }

    /**
     * GET /api/chat/health
     * Simple health check — confirms the Spring Boot service is running.
     *
     * Angular (and later a load balancer) can ping this to check
     * if the backend is alive before sending real requests.
     */
    @GetMapping("/health")
    public ResponseEntity<String> health() {
        return ResponseEntity.ok("DevAssist backend is UP");
    }
}


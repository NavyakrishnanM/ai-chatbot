package com.devassist.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

/**
 * ChatRequest DTO (Data Transfer Object)
 *
 * CONCEPT — What is a DTO?
 * A DTO is a plain object whose only job is to carry data between layers.
 * It has no business logic — just fields, validation annotations, and
 * (in Java 16+) we can use a Record which auto-generates constructor,
 * getters, equals, hashCode, and toString.
 *
 * CONCEPT — Java Records (Java 16+):
 * Instead of writing:
 *   public class ChatRequest {
 *       private String message;
 *       public ChatRequest(String message) { this.message = message; }
 *       public String getMessage() { return message; }
 *       // ... equals, hashCode, toString
 *   }
 *
 * A record gives you all of that in one line:
 *   public record ChatRequest(String message) {}
 *
 * Records are immutable — you can't change a field after construction.
 * This is ideal for DTOs which should never be mutated.
 *
 * CONCEPT — Validation annotations:
 * @NotBlank    → field must not be null or whitespace-only
 * @Size        → enforces min/max character count
 *
 * These are only activated when the controller uses @Valid on the
 * parameter. If validation fails, Spring returns 400 Bad Request
 * automatically — you don't write that error handling yourself.
 *
 * CONCEPT — Jackson (JSON serialization):
 * When Angular sends:  {"message": "What is DI?"}
 * Jackson reads that JSON and calls: new ChatRequest("What is DI?")
 * This mapping is automatic — you don't write any parsing code.
 */
public record ChatRequest(

        @NotBlank(message = "Message cannot be blank")
        @Size(max = 2000, message = "Message must be 2000 characters or fewer")
        String message

) {}


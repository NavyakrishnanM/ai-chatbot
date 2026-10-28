/**
 * ChatMessage model — represents one message in the conversation
 *
 * CONCEPT — TypeScript interfaces:
 * An interface defines the "shape" of an object. It's compile-time only
 * (disappears at runtime). Use it to get autocompletion and type safety.
 *
 * 'user'      → a message the person typed
 * 'assistant' → a reply from the AI
 * 'error'     → a failed request shown as a message bubble
 */
export interface ChatMessage {
  id: string;           // unique ID for Angular's @for track expression
  role: 'user' | 'assistant' | 'error';
  content: string;
  timestamp: Date;
}

/**
 * ChatResponse — matches the JSON Spring Boot sends back:
 * { "reply": "...", "modelUsed": "..." }
 *
 * CONCEPT — Matching backend DTOs:
 * This interface mirrors Spring Boot's ChatResponse record.
 * If the backend field name is "modelUsed" (camelCase), the interface
 * must use the same casing — Jackson and Angular's HttpClient both
 * use camelCase by convention.
 */
export interface ChatResponse {
  reply: string;
  modelUsed: string;
}


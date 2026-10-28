import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ChatResponse } from '../models/chat.model';
import { environment } from '../../../environments/environment';

/**
 * ChatService — HTTP communication layer
 *
 * CONCEPT — @Injectable({ providedIn: 'root' }):
 * This makes Angular create ONE shared instance of this service for
 * the entire app (singleton). Any component that injects ChatService
 * gets the same instance — no duplicate HTTP clients.
 *
 * 'providedIn: root' is the modern approach (Angular 6+).
 * The old way was listing it in NgModule.providers — you may see this
 * in older Angular codebases.
 *
 * CONCEPT — inject() function vs constructor injection:
 * Old style:  constructor(private http: HttpClient) {}
 * New style:  private http = inject(HttpClient);
 *
 * Both work identically. The inject() function (Angular 14+) is cleaner
 * and works in standalone components. We use this modern approach.
 *
 * CONCEPT — Why keep HTTP calls in a service, not the component?
 * Same reason as Spring Boot's Controller → Service split:
 *   - The component shouldn't know the URL
 *   - If the URL changes, you fix it in ONE place
 *   - You can mock this service in tests without real HTTP calls
 *   - Multiple components can reuse the same sendMessage() method
 */
@Injectable({
  providedIn: 'root'
})
export class ChatService {

  private http = inject(HttpClient);

  // Base URL from environment — never hardcoded
  private readonly apiUrl = `${environment.apiUrl}/api/chat`;

  /**
   * Sends a message to Spring Boot and returns an Observable of the response.
   *
   * CONCEPT — Observable vs Promise:
   * Angular's HttpClient returns Observables (from RxJS), not Promises.
   * An Observable is like a stream — it can emit one value, multiple values,
   * or an error. For a single HTTP response it behaves like a Promise,
   * but Observables give you extra powers:
   *   - cancel the request (unsubscribe)
   *   - retry on failure (pipe(retry(3)))
   *   - chain transforms (pipe(map(...)))
   *
   * In the component we'll subscribe to this Observable and handle the result.
   *
   * CONCEPT — Generic type http.post<ChatResponse>(...):
   * The <ChatResponse> tells TypeScript what type the response body is.
   * HttpClient will automatically deserialize the JSON into that type.
   * Without the generic, you'd get `any` — no type safety.
   *
   * @param message The text the user typed
   * @returns Observable that emits a ChatResponse when the API responds
   */
  sendMessage(message: string): Observable<ChatResponse> {
    return this.http.post<ChatResponse>(this.apiUrl, { message });
  }
}


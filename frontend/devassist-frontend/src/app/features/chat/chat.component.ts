import { Component, signal, inject, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../../core/services/chat.service';
import { ChatMessage } from '../../core/models/chat.model';

/**
 * ChatComponent — The main chat interface
 *
 * CONCEPT — Standalone Components (Angular 15+):
 * Previously, every component had to be declared in an NgModule.
 * With standalone:true, the component is self-contained — it declares
 * its own imports directly. No NgModule needed.
 *
 * imports: [FormsModule] — gives us [(ngModel)] for the text input
 *
 * CONCEPT — Signals (Angular 16+):
 * Signals are Angular's modern reactive state system.
 *
 *   const count = signal(0);       // create a signal with initial value 0
 *   count()                        // read — returns current value
 *   count.set(5)                   // replace the value
 *   count.update(v => v + 1)       // update based on current value
 *
 * When a signal's value changes, Angular ONLY re-renders the template
 * parts that actually read that signal. This is more efficient than
 * the old Change Detection approach.
 *
 * We use 3 signals:
 *   messages   — the list of chat messages (rendered as bubbles)
 *   isLoading  — true while waiting for the API (shows typing dots)
 *   error      — an error string if something went wrong
 *
 * CONCEPT — AfterViewChecked:
 * A lifecycle hook that runs after Angular updates the view.
 * We use it to auto-scroll the chat window to the latest message.
 */
@Component({
  selector: 'app-chat',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.css'
})
export class ChatComponent implements AfterViewChecked {

  // --- Dependency Injection ---
  private chatService = inject(ChatService);

  // --- State (Signals) ---

  /** The full conversation history shown as bubbles */
  messages = signal<ChatMessage[]>([]);

  /** True while waiting for the AI response — shows typing indicator */
  isLoading = signal(false);

  /** Non-null when an API error occurs — shown as an error bubble */
  error = signal<string | null>(null);

  // --- Local state (no signal needed — not used in template directly) ---

  /** Two-way bound to the text input via [(ngModel)] */
  inputText = '';

  /** Reference to the scroll container — used to auto-scroll */
  @ViewChild('scrollContainer') private scrollContainer!: ElementRef;

  /** Track whether we need to scroll after the view updates */
  private shouldScrollToBottom = false;

  // ---------------------------------------------------------------

  ngAfterViewChecked(): void {
    // Auto-scroll to bottom after each render cycle that added a message
    if (this.shouldScrollToBottom) {
      this.scrollToBottom();
      this.shouldScrollToBottom = false;
    }
  }

  /**
   * Called when the user clicks Send or presses Enter.
   *
   * CONCEPT — Observable.subscribe():
   * chatService.sendMessage() returns an Observable (not a value).
   * Nothing happens until you call .subscribe().
   * subscribe() takes up to 3 callbacks:
   *   next  — called when the API responds successfully
   *   error — called when the HTTP request fails (4xx, 5xx, network error)
   *   (complete — called when the observable finishes; not needed here)
   */
  sendMessage(): void {
    const message = this.inputText.trim();
    if (!message || this.isLoading()) return;  // guard: ignore empty/double sends

    // 1. Add the user's message to the chat immediately (optimistic UI)
    this.addMessage('user', message);

    // 2. Clear the input box
    this.inputText = '';

    // 3. Show the typing indicator
    this.isLoading.set(true);
    this.error.set(null);

    // 4. Call the service — subscribe to the Observable
    this.chatService.sendMessage(message).subscribe({
      next: (response) => {
        // API call succeeded — add the AI's reply
        this.addMessage('assistant', response.reply);
        this.isLoading.set(false);
      },
      error: (err) => {
        // API call failed — show an error bubble instead of a reply
        console.error('Chat API error:', err);
        const userMessage = err.status === 0
          ? 'Cannot connect to the server. Is the backend running?'
          : `Server error (${err.status}): ${err.error?.message ?? 'Something went wrong'}`;
        this.addMessage('error', userMessage);
        this.isLoading.set(false);
      }
    });
  }

  /**
   * Adds a new message object to the messages signal.
   *
   * CONCEPT — signal.update():
   * We can't mutate the array directly (that won't trigger re-render).
   * Instead, update() replaces the array with a new one containing
   * the old messages + the new one. Angular detects the new reference
   * and re-renders the @for loop.
   */
  private addMessage(role: 'user' | 'assistant' | 'error', content: string): void {
    const newMessage: ChatMessage = {
      id: crypto.randomUUID(),  // unique key for Angular's @for track
      role,
      content,
      timestamp: new Date()
    };
    this.messages.update(msgs => [...msgs, newMessage]);
    this.shouldScrollToBottom = true;
  }

  private scrollToBottom(): void {
    try {
      const el = this.scrollContainer.nativeElement;
      el.scrollTop = el.scrollHeight;
    } catch (_) {}
  }

  /** Formats a Date as HH:MM for display next to each message */
  formatTime(date: Date): string {
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false });
  }
}


import { ApplicationConfig, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { routes } from './app.routes';

/**
 * App Configuration — the root providers for the entire application.
 *
 * CONCEPT — provideHttpClient():
 * This registers Angular's HttpClient service into the dependency
 * injection system. Without this line, injecting HttpClient anywhere
 * in the app would throw a runtime error:
 *   "NullInjectorError: No provider for HttpClient"
 *
 * It's the Angular equivalent of Spring Boot's @Bean RestClient.Builder
 * auto-configuration — you declare it once, use it everywhere via inject().
 *
 * CONCEPT — Why is this in app.config.ts and not the component?
 * Providers registered here are available to the ENTIRE application.
 * If you add it only to a specific component's imports, only that
 * component and its children can use HttpClient.
 */
export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes),
    provideHttpClient()   // ← enables HttpClient everywhere in the app
  ]
};

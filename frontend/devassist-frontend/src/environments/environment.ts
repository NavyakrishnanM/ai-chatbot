/**
 * Environment configuration — Development
 *
 * CONCEPT — Environment files:
 * Angular supports multiple environments: dev, staging, production.
 * angular.json maps environment.ts → environment.prod.ts at build time
 * when you run: ng build --configuration=production
 *
 * This means you NEVER hardcode the API URL in your services.
 * You change one file (or use CI/CD to swap it) and the whole app updates.
 *
 * The backend URL points to Spring Boot (port 8080).
 * Spring Boot then forwards to Python (port 8000) internally.
 * Angular only ever knows about Spring Boot — not Python directly.
 * That's the value of the middle layer.
 */
export const environment = {
  production: false,
  apiUrl: 'http://localhost:8080'
};


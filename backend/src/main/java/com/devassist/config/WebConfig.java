package com.devassist.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

/**
 * WebConfig — CORS Configuration
 *
 * CONCEPT — What is CORS?
 * CORS (Cross-Origin Resource Sharing) is a browser security feature.
 * By default, browsers BLOCK JavaScript from calling a different origin.
 *
 * Our origins:
 *   Angular frontend  → http://localhost:4200   (origin A)
 *   Spring Boot API   → http://localhost:8080   (origin B)
 *
 * When Angular at port 4200 calls Spring Boot at port 8080, the browser
 * sees a "cross-origin" request and blocks it — UNLESS the server
 * explicitly says "I allow requests from localhost:4200".
 *
 * This class tells Spring Boot: "Accept requests from Angular's origin."
 *
 * IMPORTANT: CORS is enforced by the BROWSER, not by curl/Postman/Python.
 * That's why Postman tests work without CORS config but the Angular app
 * would fail without it.
 *
 * CONCEPT — @Configuration:
 * Marks this as a Spring configuration class (like a @Bean factory).
 * Spring reads it at startup and applies the CORS rules.
 */
@Configuration
public class WebConfig implements WebMvcConfigurer {

    // Read the allowed origin from application.properties
    // In production this would be your real domain e.g. https://devassist.io
    @Value("${frontend.url:http://localhost:4200}")
    private String frontendUrl;

    /**
     * Configure CORS rules for all API endpoints.
     *
     * addMapping("/**")          → apply this rule to ALL endpoints
     * allowedOrigins(...)        → which frontend URLs can call us
     * allowedMethods(...)        → which HTTP verbs are allowed
     * allowedHeaders("*")        → allow any request headers
     * allowCredentials(true)     → allow cookies (needed for JWT later)
     * maxAge(3600)               → cache the preflight response for 1 hour
     *                              (reduces OPTIONS preflight requests)
     */
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOrigins(frontendUrl)
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowedHeaders("*")
                .allowCredentials(true)
                .maxAge(3600);
    }
}


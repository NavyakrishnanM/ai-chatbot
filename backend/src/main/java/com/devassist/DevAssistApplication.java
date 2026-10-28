package com.devassist;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * DevAssist Application Entry Point
 *
 * CONCEPT — @SpringBootApplication:
 * This single annotation is actually three annotations combined:
 *
 *   @Configuration      → This class can define Spring beans
 *   @EnableAutoConfiguration → Spring Boot reads your classpath and
 *                              auto-configures things (e.g. sees spring-web
 *                              on classpath → auto-starts Tomcat on port 8080)
 *   @ComponentScan      → Scans this package and sub-packages for
 *                         @Controller, @Service, @Repository, etc.
 *
 * When you run main(), Spring Boot:
 *   1. Starts the embedded Tomcat server
 *   2. Scans for components and wires them via dependency injection
 *   3. Applies auto-configuration based on classpath
 *   4. Your app is ready to serve requests
 */
@SpringBootApplication
public class DevAssistApplication {

    public static void main(String[] args) {
        SpringApplication.run(DevAssistApplication.class, args);
    }

}


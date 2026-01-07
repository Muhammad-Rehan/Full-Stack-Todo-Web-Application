# Claude Code Rules - Backend

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in backend development for the Todo Full-Stack Web Application.

## Task context

**Your Surface:** You operate on the backend level, focusing on FastAPI, SQLModel, database operations, and server-side functionality.

**Your Success is Measured By:**
- All backend code follows FastAPI best practices (Pydantic models, dependency injection)
- Database operations are efficient and secure
- API endpoints follow RESTful conventions
- Authentication and authorization are properly implemented

## Core Guarantees (Product Promise)

- All API endpoints have proper validation and error handling
- Database models follow SQLModel conventions
- Authentication is secure and properly implemented
- API documentation is automatically generated

## Development Guidelines

### 1. Backend Technology Stack:
- FastAPI 0.104+ with Pydantic v2
- SQLModel for ORM and validation
- PostgreSQL database with Neon
- JWT-based authentication

### 2. Database Operations:
- Use SQLModel for all database operations
- Implement proper database session management
- Use async database operations where possible
- Follow ACID principles for transactions

### 3. API Design:
- Follow RESTful API conventions
- Use proper HTTP status codes
- Implement comprehensive request validation
- Provide clear API documentation

### 4. Security Implementation:
- Implement JWT token authentication
- Validate all user inputs
- Use parameterized queries to prevent SQL injection
- Follow OWASP API security best practices

## Default policies (must follow)
- Use async/await for all I/O operations
- Implement proper error handling and logging
- Follow security best practices for authentication
- Use Pydantic models for request/response validation
- Follow FastAPI dependency injection patterns
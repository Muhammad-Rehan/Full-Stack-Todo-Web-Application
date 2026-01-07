Backend Architect Skill

## Metadata
name: backend-architect
description: Use for server-side architecture, API design, database modeling, authentication, business logic, and Python backend implementation

## Overview
This Skill provides specialized backend architecture expertise for the Todo Full-Stack Web Application. When implementing backend features, API design, database models, authentication systems, or business logic, apply these architectural principles and best practices. Claude should reference these guidelines whenever creating backend components to ensure proper architecture, security, and maintainability.

## Technology Stack

- FastAPI for web framework
- SQLModel for ORM and validation
- PostgreSQL with Neon Serverless
- JWT-based authentication
- Python 3.11+

## Architecture Principles

- Clean separation between API, services, and data access layers
- Follow RESTful API conventions with proper HTTP semantics
- Implement proper error handling and logging
- Use dependency injection for service layers
- Follow security best practices (OWASP API security)

## Database Design

- Use SQLModel for type-safe database operations
- Implement proper relationships and constraints
- Follow ACID principles for transactions
- Use async database operations where possible
- Implement proper indexing strategies

## API Design Standards

- Use Pydantic models for request/response validation
- Implement comprehensive request validation
- Provide clear API documentation
- Use proper HTTP status codes
- Follow consistent error response formats

## Security Implementation

- Implement JWT token authentication
- Validate all user inputs
- Use parameterized queries to prevent SQL injection
- Follow OWASP API security best practices
- Implement proper access control and authorization

## When to Apply

Apply these guidelines whenever implementing:
- API endpoint design
- Database model creation
- Authentication systems
- Business logic services
- Security measures
- Backend architectural decisions

## Code Standards

- Use async/await for all I/O operations
- Implement proper error handling and logging
- Follow FastAPI dependency injection patterns
- Use type hints for all functions
- Write comprehensive tests for critical functionality
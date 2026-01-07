Todo App Architect Skill

## Metadata
name: todo-app-architect
description: Use for full-stack architecture decisions in the Todo Full-Stack Web Application

## Overview
This Skill provides comprehensive architectural guidance for the Todo Full-Stack Web Application (Phase II). When making architectural decisions that span both frontend and backend, or when implementing features that require coordination between both sides, apply these architectural principles and best practices. Claude should reference these guidelines to ensure consistent architecture across the full stack.

## Project Architecture

- Monorepo structure with separate frontend/ and backend/ directories
- Next.js frontend with App Router
- FastAPI backend with SQLModel ORM
- PostgreSQL database with Neon Serverless
- JWT-based authentication system
- RESTful API design principles

## Cross-Cutting Concerns

- Authentication and authorization spanning both frontend and backend
- Data consistency between client and server
- Error handling patterns across the stack
- Security measures on both sides
- Performance optimization strategies

## Integration Patterns

- API contract design between frontend and backend
- State management coordination
- Authentication token handling across both systems
- Data validation consistency
- Error response handling patterns

## When to Apply

Apply these guidelines whenever implementing:
- Full-stack feature development
- API contract design
- Authentication flow implementation
- Cross-cutting concerns
- Architecture decisions affecting both frontend and backend
- Integration between frontend and backend components

## Quality Standards

- Maintain consistent coding standards across both frontend and backend
- Ensure proper separation of concerns
- Follow security best practices throughout the stack
- Implement proper testing strategies for both sides
- Maintain consistent error handling and logging
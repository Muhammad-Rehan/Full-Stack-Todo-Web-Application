# Claude Code Rules - Frontend

This file is generated during init for the selected agent.

You are an expert AI assistant specializing in frontend development for the Todo Full-Stack Web Application.

## Task context

**Your Surface:** You operate on the frontend level, focusing on Next.js, React, UI/UX, and client-side functionality.

**Your Success is Measured By:**
- All frontend code follows Next.js best practices (App Router, Server vs Client Components)
- UI is responsive and accessible
- API calls are properly integrated with error handling
- Frontend security best practices are maintained

## Core Guarantees (Product Promise)

- All components are reusable and well-documented
- API integration follows security best practices
- Responsive design works across all device sizes
- Accessibility standards (WCAG) are met

## Development Guidelines

### 1. Frontend Technology Stack:
- Next.js 14+ with App Router
- React 18+ with TypeScript
- Tailwind CSS for styling
- Server Components by default, Client Components only when interactivity is needed

### 2. API Integration:
- Use fetch or axios for API calls
- Implement proper error handling and loading states
- Securely handle JWT tokens in requests
- Follow RESTful API conventions

### 3. Component Architecture:
- Create reusable, well-structured components
- Separate presentational and container components
- Use proper TypeScript interfaces for props
- Implement proper state management

### 4. Security Considerations:
- Never expose sensitive data in client-side code
- Properly handle authentication tokens
- Validate user input before sending to backend
- Follow OWASP frontend security best practices

## Default policies (must follow)
- Use Server Components by default, Client Components only when necessary
- Follow accessibility best practices (ARIA labels, semantic HTML)
- Implement responsive design patterns
- Use TypeScript for type safety
- Follow Next.js conventions and best practices
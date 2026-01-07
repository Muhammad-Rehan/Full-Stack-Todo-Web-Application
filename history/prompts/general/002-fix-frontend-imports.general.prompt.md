---
id: "002"
title: "Fix Frontend Import Issues and 404 Error"
stage: "general"
date: "2026-01-02"
surface: "agent"
model: "claude-opus-4-5-20251101"
feature: "none"
branch: "master"
user: "user"
command: "fix-frontend-imports"
labels: ["frontend", "bug-fix", "context", "imports"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "frontend/src/app/auth/signin/page.tsx"
  - "frontend/src/app/auth/signup/page.tsx"
  - "frontend/src/app/auth/page.tsx"
  - "frontend/src/components/Navbar.tsx"
  - "frontend/src/components/auth/LoginForm.tsx"
  - "frontend/src/components/auth/SignupForm.tsx"
  - "frontend/src/components/tasks/TaskForm.tsx"
  - "frontend/src/components/tasks/TaskItem.tsx"
  - "frontend/src/services/api.ts"
  - "frontend/src/contexts/AuthContext.tsx"
  - "frontend/src/contexts/TaskContext.tsx"
  - "frontend/src/components/auth/AuthProvider.tsx"
  - "frontend/src/components/tasks/TaskProvider.tsx"
tests:
  - "frontend/__tests__/TaskForm.test.tsx"
  - "frontend/__tests__/TaskList.test.tsx"
---

# Fix Frontend Import Issues and 404 Error

## Summary

Fixed import issues and 404 error in the frontend by migrating all components from the old separate AuthContext and TaskContext to the unified AppContext. Removed redundant context providers that were causing conflicts.

## User Intent

User reported that the frontend was showing 404 pages and had import issues when running both frontend and backend.

## Implementation Details

### Issues Identified
- Multiple authentication contexts were causing conflicts
- Components were using old `useAuth` and `useTasks` hooks from separate contexts
- Old context files were conflicting with the new unified AppContext

### Changes Made
1. Updated all authentication pages (signin, signup) to use `useApp` instead of `useAuth`
2. Updated Navbar component to use the unified context
3. Updated auth forms (LoginForm, SignupForm) to use the new context
4. Updated task components (TaskForm, TaskItem) to use the new context
5. Fixed API service to remove unnecessary imports and add missing methods
6. Removed redundant context files that were no longer needed:
   - AuthContext.tsx
   - TaskContext.tsx
   - AuthProvider.tsx
   - TaskProvider.tsx

### Key Updates
- `frontend/src/app/auth/signin/page.tsx` - Updated to use `useApp`
- `frontend/src/app/auth/signup/page.tsx` - Updated to use `useApp`
- `frontend/src/components/Navbar.tsx` - Updated to use `useApp`
- `frontend/src/components/tasks/TaskForm.tsx` - Updated to use `useApp` instead of `useTasks`
- `frontend/src/components/tasks/TaskItem.tsx` - Updated to use `useApp` instead of `useTasks`

## Outcome

All import issues have been resolved and the frontend should now work correctly with the unified AppContext. The application now properly uses a single context for both authentication and task management, eliminating conflicts between multiple contexts.

## Validation

All components now consistently use the unified AppContext, eliminating context conflicts that were causing the 404 and import issues. The application should now run properly with both frontend and backend.
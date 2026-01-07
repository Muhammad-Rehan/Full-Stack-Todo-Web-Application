# Quick Start Guide - Todo Full-Stack Web Application

This guide will help you get the Todo Full-Stack Web Application up and running quickly.

## Prerequisites

- Python 3.11+ installed
- Node.js 18+ installed (for frontend)
- PostgreSQL server or Neon Serverless account

## Installation Steps

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <repo-name>
```

### 2. Set up the backend

Navigate to the backend directory:

```bash
cd backend
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the backend directory with the following variables:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
NEON_DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/todo_app?sslmode=require
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
BETTER_AUTH_SECRET=your-better-auth-secret-change-in-production
BETTER_AUTH_URL=http://localhost:3000
FRONTEND_URL=http://localhost:3000
```

### 4. Run database migrations

If using Alembic for migrations:

```bash
alembic upgrade head
```

### 5. Start the backend server

```bash
python -m uvicorn src.main:app --reload
```

The backend API will be available at `http://localhost:8000`.

### 6. Set up the frontend (optional)

If you want to run the frontend:

```bash
cd ../frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## API Usage

### Authentication

To register a new user:

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

To sign in:

```bash
curl -X POST http://localhost:8000/api/auth/signin \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword"
  }'
```

### Working with Tasks

Once authenticated and with a JWT token, you can work with tasks:

Get all tasks:

```bash
curl -X GET http://localhost:8000/api/tasks \
  -H "Authorization: Bearer <your-jwt-token>"
```

Create a new task:

```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{
    "title": "My new task",
    "description": "Task description",
    "completed": false
  }'
```

## Testing

Run backend tests:

```bash
cd backend
python -m pytest
```

## Troubleshooting

### Common Issues

1. **Database Connection Error**: Ensure PostgreSQL is running and credentials in `.env` are correct.

2. **JWT Secret Issues**: Make sure `JWT_SECRET_KEY` is set in your environment variables.

3. **Port Already in Use**: Change the port in the uvicorn command if 8000 is already in use.

## Next Steps

- Implement the frontend to interact with the API
- Set up production deployment configurations
- Add more comprehensive tests
- Implement additional features as per the specification
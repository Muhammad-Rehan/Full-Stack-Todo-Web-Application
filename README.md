# Todo Full-Stack Web Application (Phase II)

A multi-user, full-stack todo web application with persistent storage, authentication, and RESTful APIs.

## Features

- User authentication and registration with JWT tokens
- Create, read, update, and delete personal tasks
- Secure access control (users can only access their own tasks)
- RESTful API with proper error handling
- PostgreSQL database with Neon Serverless support

## Tech Stack

- **Frontend**: Next.js 14+ with App Router
- **Backend**: FastAPI with Python 3.11+
- **Database**: PostgreSQL with SQLModel ORM
- **Authentication**: JWT-based with custom middleware
- **Deployment**: GitHub Pages (via GitHub Actions) or modern cloud platforms

## Project Structure

```
├── backend/                 # FastAPI backend
│   ├── src/
│   │   ├── models/         # SQLModel database models
│   │   ├── services/       # Business logic services
│   │   ├── api/            # API route definitions
│   │   ├── auth/           # Authentication utilities
│   │   └── database.py     # Database configuration
│   ├── requirements.txt
│   └── alembic/            # Database migrations
├── frontend/               # Next.js frontend
│   ├── src/
│   └── package.json
├── specs/01-todo-web-app/  # Feature specifications
├── .env                    # Environment variables
├── .gitignore             # Git ignore rules
├── pyproject.toml         # Python project configuration
└── package.json           # Root monorepo configuration
```

## Setup

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (or Neon Serverless account)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables in `.env`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
```

4. Run the application:
```bash
python -m uvicorn src.main:app --reload
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

## API Endpoints

### Authentication

- `POST /api/auth/signup` - Create a new user account
- `POST /api/auth/signin` - Authenticate user and return JWT token

### Tasks

- `GET /api/tasks` - Get all tasks for authenticated user
- `POST /api/tasks` - Create a new task for authenticated user
- `GET /api/tasks/{task_id}` - Get a specific task by ID
- `PUT /api/tasks/{task_id}` - Update a specific task by ID
- `DELETE /api/tasks/{task_id}` - Delete a specific task by ID
- `PATCH /api/tasks/{task_id}/toggle` - Toggle completion status of a task

## Environment Variables

The application uses the following environment variables:

- `DATABASE_URL` - PostgreSQL database connection string
- `JWT_SECRET_KEY` - Secret key for JWT token signing
- `JWT_ALGORITHM` - Algorithm for JWT token signing (default: HS256)
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time in minutes

## Database Migrations

This project uses Alembic for database migrations:

1. To create a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

2. To apply migrations:
```bash
alembic upgrade head
```

## Testing

Run backend tests with pytest:
```bash
cd backend
python -m pytest
```

## Security

- All API endpoints require valid JWT authentication tokens
- Users can only access their own tasks
- Passwords are securely hashed using bcrypt
- Input validation is performed on all endpoints

## Development

This project follows the Spec-Driven Development approach with specifications in the `specs/` directory. All development should align with the defined specifications, plans, and tasks.

## Deployment

### GitHub Pages Deployment

This project is configured to automatically deploy to GitHub Pages when changes are pushed to the main branch. The deployment is handled by the GitHub Actions workflow defined in `.github/workflows/github-pages.yml`.

### Manual Deployment

To build and export the frontend manually for static hosting:

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Build and export the static site:
```bash
npm run export
```

The built site will be available in the `out/` directory.

### Backend Deployment

The backend FastAPI application can be deployed to any cloud platform that supports Python applications (e.g., Heroku, Railway, AWS, GCP, etc.). You'll need to configure environment variables for database connection and JWT secrets.
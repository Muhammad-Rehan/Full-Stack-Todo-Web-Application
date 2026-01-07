# Quickstart Guide: Todo Full-Stack Web Application (Phase II)

## Prerequisites
- Node.js 18+ for frontend
- Python 3.11+ for backend
- PostgreSQL client tools
- Git

## Setup Instructions

### 1. Clone and Initialize
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastapi sqlmodel python-jose[cryptography] passlib[bcrypt] python-multipart uvicorn
```

### 3. Frontend Setup
```bash
cd frontend
npm install next react react-dom @types/react @types/node
```

### 4. Environment Configuration
Create `.env` files for both frontend and backend with required configuration:
- Database connection string
- JWT secret
- Better Auth configuration

### 5. Database Setup
```bash
# Run database migrations
cd backend
python -c "from src.db import create_db_and_tables; create_db_and_tables()"
```

### 6. Run the Application
Backend:
```bash
cd backend
uvicorn src.main:app --reload
```

Frontend:
```bash
cd frontend
npm run dev
```

## Development Workflow
1. Make changes to backend in `backend/src/`
2. Make changes to frontend in `frontend/src/`
3. Run backend tests: `pytest`
4. Run frontend tests: `npm test`
5. Both applications available at specified ports (typically 8000 for backend, 3000 for frontend)
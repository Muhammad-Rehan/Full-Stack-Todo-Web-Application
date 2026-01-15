# src/main.py
from fastapi import FastAPI, Request, Response
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from fastapi.middleware.cors import CORSMiddleware
import logging

from src.config import settings                        # absolute import
from src.database import get_engine, create_db_and_tables
from src.api.auth import router as auth_router
from src.api.tasks import router as tasks_router
from src.middleware.performance import PerformanceMonitoringMiddleware

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# CORS origins — only scheme + domain (no paths)
# Use the frontend_url from settings, plus localhost for development
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
if settings.frontend_url:
    ALLOWED_ORIGINS.append(settings.frontend_url)

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
    )

    # -------------------------------
    # ✅ CORS middleware must come first
    # -------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -------------------------------
    # ✅ Global OPTIONS handler for preflight requests
    # -------------------------------
    @app.options("/{full_path:path}")
    async def preflight(full_path: str, request: Request):
        # Return proper CORS headers for preflight
        response = Response(status_code=200)
        origin = request.headers.get("origin")
        if origin and any(allowed_origin == origin or allowed_origin == "*" for allowed_origin in ALLOWED_ORIGINS):
            response.headers["Access-Control-Allow-Origin"] = origin
        else:
            # If origin is not in allowed list, use first allowed origin (or handle as needed)
            if ALLOWED_ORIGINS:
                response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGINS[0]

        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, PATCH, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type, Set-Cookie"
        return response

    # -------------------------------
    # ✅ Custom middleware (after CORS)
    # -------------------------------
    app.add_middleware(PerformanceMonitoringMiddleware)

    # Log allowed origins
    logger.info(f"CORS allowed origins: {ALLOWED_ORIGINS}")

    # -------------------------------
    # Routers
    # -------------------------------
    app.include_router(auth_router, prefix="/api")  # /api/auth
    app.include_router(tasks_router, prefix="/api")  # /api/tasks

    # -------------------------------
    # Startup event
    # -------------------------------
    @app.on_event("startup")
    def on_startup():
        logger.info("Testing database connection...")
        try:
            engine = get_engine()
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            logger.info("Database connection successful.")
            create_db_and_tables()
            logger.info("Database tables ensured.")
        except OperationalError as e:
            logger.error("Database connection failed.")
            logger.error(str(e))
            raise RuntimeError(
                "Cannot connect to database. Check DATABASE_URL, credentials, and host."
            ) from e

    # -------------------------------
    # Health endpoint
    # -------------------------------
    @app.get("/")
    def health():
        return {"status": "ok", "service": settings.app_name}

    return app


# Instantiate app
app = create_app()

# Local dev runner
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",      # updated for absolute path
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )

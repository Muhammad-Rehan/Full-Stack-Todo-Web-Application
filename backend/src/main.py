# src/main.py
from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from fastapi.middleware.cors import CORSMiddleware
import logging

from .config import settings
from .database import engine, create_db_and_tables
from .api.auth import router as auth_router
from .api.tasks import router as tasks_router
from .middleware.performance import PerformanceMonitoringMiddleware

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of allowed origins for frontend
ALLOWED_ORIGINS = [
    settings.frontend_url if hasattr(settings, 'frontend_url') and settings.frontend_url else "http://localhost:3000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Ensure no duplicates and handle potential None values
ALLOWED_ORIGINS = [origin for origin in ALLOWED_ORIGINS if origin is not None]
ALLOWED_ORIGINS = list(set(ALLOWED_ORIGINS))

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
    )

    # Middleware
    app.add_middleware(PerformanceMonitoringMiddleware)

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info(f"CORS allowed origins: {ALLOWED_ORIGINS}")

    # Routers
    app.include_router(auth_router, prefix="/api")  # Add /api prefix to match frontend expectation
    app.include_router(tasks_router, prefix="/api")  # Add /api prefix to match frontend expectation

    # Startup event
    @app.on_event("startup")
    def on_startup():
        logger.info("Testing database connection...")
        try:
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

    # Health endpoint
    @app.get("/")
    def health():
        return {"status": "ok", "service": settings.app_name}

    return app


# Instantiate the FastAPI app
app = create_app()

# Run using uvicorn if executed directly
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )

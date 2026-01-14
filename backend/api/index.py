from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
import os

# Add the current directory's parent to the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from config import settings
from database import get_engine, create_db_and_tables
from api.auth import router as auth_router
from api.tasks import router as tasks_router
from middleware.performance import PerformanceMonitoringMiddleware

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Allowed CORS origins (NO paths)
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://muhammad-rehan.github.io",
]

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
    )

    # -------------------------------
    # CORS middleware (ONLY place CORS is handled)
    # -------------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # -------------------------------
    # Custom middleware
    # -------------------------------
    app.add_middleware(PerformanceMonitoringMiddleware)

    logger.info(f"CORS allowed origins: {ALLOWED_ORIGINS}")

    # -------------------------------
    # Routers
    # -------------------------------
    app.include_router(auth_router, prefix="/api")
    app.include_router(tasks_router, prefix="/api")

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
                "Cannot connect to database. Check DATABASE_URL and credentials."
            ) from e

    # -------------------------------
    # Health check
    # -------------------------------
    @app.get("/")
    def health():
        return {"status": "ok", "service": settings.app_name}

    return app


# Required for Vercel
app = create_app()

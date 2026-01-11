# src/main.py
from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.requests import Request
import logging

from .config import settings
from .database import get_engine, create_db_and_tables
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
    "https://muhammad-rehan.github.io",  # GitHub Pages deployment
    "https://muhammad-rehan.github.io/Full-Stack-Todo-Web-Application",  # Specific GitHub Pages path
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
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        # Allow all headers including authorization
        allow_origin_regex=r"https://.*\.github\.io(/.*)?",
    )

    # Additional custom middleware to ensure CORS headers are set
    async def cors_middleware(request: Request, call_next):
        response = await call_next(request)

        # Always set CORS headers for all responses
        origin = request.headers.get("origin")
        if origin and any(allowed_origin in origin or
                         origin.endswith(allowed_domain) for allowed_origin in ALLOWED_ORIGINS
                         for allowed_domain in [".github.io", "muhammad-rehan.github.io"]):
            response.headers["Access-Control-Allow-Origin"] = origin
        else:
            # Fallback to specific allowed origins
            response.headers["Access-Control-Allow-Origin"] = "https://muhammad-rehan.github.io"

        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Headers"] = request.headers.get("Access-Control-Request-Headers", "*")
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"

        return response

    app.middleware("http")(cors_middleware)
    logger.info(f"CORS allowed origins: {ALLOWED_ORIGINS}")

    # Routers
    app.include_router(auth_router, prefix="/api")  # Add /api prefix to match frontend expectation
    app.include_router(tasks_router, prefix="/api")  # Add /api prefix to match frontend expectation

    # Startup event
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

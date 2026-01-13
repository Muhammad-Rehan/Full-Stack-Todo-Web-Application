from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from api.config import settings
from api.database import create_db_and_tables
from api.auth import router as auth_router
from api.tasks import router as tasks_router

logger = logging.getLogger(__name__)

# -----------------------------
# Initialize FastAPI app
# -----------------------------
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],  # your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Include Routers
# -----------------------------
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(tasks_router, prefix="/api/tasks", tags=["tasks"])

# -----------------------------
# Startup Event: Create DB
# -----------------------------
@app.on_event("startup")
async def on_startup():
    logger.info("Starting up: creating tables if needed...")
    create_db_and_tables()
    logger.info("Startup complete.")

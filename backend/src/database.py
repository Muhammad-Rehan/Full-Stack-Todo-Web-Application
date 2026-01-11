# src/database.py
from sqlmodel import Session, SQLModel
from typing import Generator
from .config import settings
import logging

logger = logging.getLogger(__name__)

# ---------------------------------
# Lazy Engine Creation for Serverless
# ---------------------------------
def get_engine():
    from sqlmodel import create_engine

    # Create engine only when needed (lazy initialization)
    engine = create_engine(
        settings.database_url,
        echo=True,
        pool_pre_ping=True,
        # Use smaller pool sizes for serverless
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=300,
        connect_args={
            "sslmode": "require",
            # Additional connection args for serverless
            "connect_timeout": 10,
        },
    )
    return engine


# ---------------------------------
# Session Dependency
# ---------------------------------
def get_session() -> Generator[Session, None, None]:
    engine = get_engine()
    with Session(engine) as session:
        yield session

# ---------------------------------
# Create Tables
# ---------------------------------
def create_db_and_tables() -> None:
    from .models.user import User
    from .models.task import Task

    logger.info("Creating database tables if not present...")
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables ready.")

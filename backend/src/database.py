# src/database.py
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
from .config import settings
import logging

logger = logging.getLogger(__name__)

# ---------------------------------
# Create SQLAlchemy Engine (SYNC)
# ---------------------------------
engine = create_engine(
    settings.database_url,
    echo=True,
    pool_pre_ping=True,
    connect_args={"sslmode": "require"},
)

# ---------------------------------
# Session Dependency
# ---------------------------------
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

# ---------------------------------
# Create Tables
# ---------------------------------
def create_db_and_tables() -> None:
    from .models.user import User
    from .models.task import Task

    logger.info("Creating database tables if not present...")
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables ready.")

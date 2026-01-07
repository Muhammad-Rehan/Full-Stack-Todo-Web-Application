import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from typing import Generator
from unittest.mock import patch

from src.main import create_app
from src.database import get_session, engine
from src.models.user import User
from src.models.task import Task


@pytest.fixture(name="engine")
def engine_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        yield session

    app = create_app()

    # Override the dependency to use our test session
    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client

    # Clean up the dependency override
    app.dependency_overrides.clear()
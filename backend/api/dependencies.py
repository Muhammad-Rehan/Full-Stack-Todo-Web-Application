from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from typing import Generator
from backend.database import get_session, get_engine
from backend.auth.middleware import JWTBearer
import uuid


# Create a reusable JWT bearer instance
jwt_bearer = JWTBearer()


def get_db_session() -> Generator[Session, None, None]:
    """
    Get database session for dependency injection
    """
    engine = get_engine()
    with Session(engine) as session:
        yield session


def get_current_user(token_data: dict = Depends(jwt_bearer)) -> dict:
    """
    Get current user from JWT token
    """
    try:
        # token_data is already the decoded payload from JWT
        user_id = token_data.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token_data
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_id(token_data: dict = Depends(jwt_bearer)) -> uuid.UUID:
    """
    Get current user ID from JWT token
    """
    try:
        # token_data is already the decoded payload from JWT
        user_id_str = token_data.get("sub")
        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return uuid.UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token",
            headers={"WWW-Authenticate": "Bearer"},
        )
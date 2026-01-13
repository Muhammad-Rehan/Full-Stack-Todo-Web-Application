from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session
from typing import Dict
from datetime import timedelta
import sys
import os

# Add the parent directory to the Python path for Vercel deployment
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from models.user import UserCreate
from auth.utils import create_access_token
from database import get_session
from config import settings
from services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Authentication"])

# -------------------------------
# Explicit OPTIONS handler for CORS preflight
# -------------------------------
@router.options("/{path:path}")
def preflight_handler(path: str):
    """
    Handles OPTIONS requests for CORS preflight.
    """
    return Response(status_code=200)


# -------------------------------
# Signup endpoint
# -------------------------------
@router.post("/signup", response_model=Dict[str, str])
def signup(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user and return access token.
    """
    user = UserService.create_user(session, user_data)

    access_token_expires = timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )
    access_token = create_access_token(
        data={"sub": str(user.user_id)},
        expires_delta=access_token_expires,
    )

    return {
        "user_id": str(user.user_id),
        "email": user.email,
        "token": access_token,
    }


# -------------------------------
# Signin endpoint
# -------------------------------
@router.post("/signin", response_model=Dict[str, str])
def signin(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Authenticate a user and return JWT token.
    """
    user = UserService.authenticate_user(
        session,
        user_data.email,
        user_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token_expires = timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )
    access_token = create_access_token(
        data={"sub": str(user.user_id)},
        expires_delta=access_token_expires,
    )

    return {
        "user_id": str(user.user_id),
        "email": user.email,
        "token": access_token,
    }

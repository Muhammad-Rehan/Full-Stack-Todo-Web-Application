# src/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session
from typing import Dict
from datetime import timedelta

from api.models.user import UserCreate              # absolute import
from api.auth.utils import create_access_token
from api.database import get_session
from api.config import settings
from api.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Authentication"])

# ✅ Explicit OPTIONS handler (NO dependencies)
@router.options("/{path:path}")
def preflight_handler(path: str):
    return Response(status_code=200)


@router.post("/signup", response_model=Dict[str, str])
def signup(user_data: UserCreate, session: Session = Depends(get_session)):
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


@router.post("/signin", response_model=Dict[str, str])
def signin(user_data: UserCreate, session: Session = Depends(get_session)):
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

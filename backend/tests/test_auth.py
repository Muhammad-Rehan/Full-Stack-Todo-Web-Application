import pytest
from fastapi.testclient import TestClient
from src.models.user import UserCreate
from src.auth.utils import create_access_token
from datetime import timedelta
from src.config import settings


def test_signup(client: TestClient):
    """Test user signup endpoint"""
    response = client.post(
        "/api/auth/signup",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert data["email"] == "test@example.com"
    assert "token" in data


def test_signin_success(client: TestClient):
    """Test successful user signin"""
    # First, create a user
    signup_response = client.post(
        "/api/auth/signup",
        json={
            "email": "login@example.com",
            "password": "testpassword123"
        }
    )
    assert signup_response.status_code == 200

    # Now try to sign in
    response = client.post(
        "/api/auth/signin",
        json={
            "email": "login@example.com",
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert data["email"] == "login@example.com"
    assert "token" in data


def test_signin_invalid_credentials(client: TestClient):
    """Test signin with invalid credentials"""
    response = client.post(
        "/api/auth/signin",
        json={
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
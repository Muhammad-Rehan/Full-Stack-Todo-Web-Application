import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_root_endpoint(client):
    """Test the root endpoint returns the correct response"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["message"] == "Todo API"


def test_auth_routes_exist(client):
    """Test that auth routes are properly registered"""
    # Test that we get proper 422 (validation error) or 401 (auth required)
    # rather than 404 (not found) for auth endpoints
    response = client.post("/api/auth/signup")
    # Should get 422 for missing/invalid request body, not 404 for not found
    assert response.status_code in [401, 422, 400]


def test_tasks_routes_exist(client):
    """Test that tasks routes are properly registered"""
    # Test that we get 401 (auth required) rather than 404 (not found) for tasks endpoints
    response = client.get("/api/tasks")
    # Should get 401 for missing auth, not 404 for not found
    assert response.status_code == 401
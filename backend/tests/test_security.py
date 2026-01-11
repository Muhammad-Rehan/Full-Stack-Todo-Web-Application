import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from uuid import UUID
from src.main import app
from src.database import get_engine
from src.models.user import User
from src.models.task import Task
from src.auth.utils import create_access_token


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def setup_test_data():
    # Create test users and tasks
    db_engine = get_engine()
    with Session(db_engine) as session:
        # Clear existing data
        session.exec(select(User))
        session.exec(select(Task))

        # Create test users
        user1 = User(email="user1@example.com", password_hash="hashed_password1")
        user2 = User(email="user2@example.com", password_hash="hashed_password2")

        session.add(user1)
        session.add(user2)
        session.commit()
        session.refresh(user1)
        session.refresh(user2)

        # Create tasks for user1
        task1 = Task(title="User1 Task 1", description="Description 1", user_id=user1.user_id)
        task2 = Task(title="User1 Task 2", description="Description 2", user_id=user1.user_id)
        session.add(task1)
        session.add(task2)
        session.commit()
        session.refresh(task1)
        session.refresh(task2)

        return user1, user2, task1, task2


def test_user_cannot_access_other_users_tasks(client, setup_test_data):
    """T049: Test that users cannot access tasks belonging to other users"""
    user1, user2, task1, task2 = setup_test_data

    # Generate tokens for both users
    user1_token = create_access_token(data={"sub": str(user1.user_id)})
    user2_token = create_access_token(data={"sub": str(user2.user_id)})

    # User2 tries to access User1's task - should fail
    response = client.get(
        f"/api/tasks/{task1.id}",
        headers={"Authorization": f"Bearer {user2_token}"}
    )

    assert response.status_code == 404  # Task not found for this user


def test_user_can_access_own_tasks(client, setup_test_data):
    """T050: Test that users can access tasks they own"""
    user1, user2, task1, task2 = setup_test_data

    # Generate token for user1
    user1_token = create_access_token(data={"sub": str(user1.user_id)})

    # User1 accesses their own task - should succeed
    response = client.get(
        f"/api/tasks/{task1.id}",
        headers={"Authorization": f"Bearer {user1_token}"}
    )

    assert response.status_code == 200
    assert response.json()["id"] == str(task1.id)
    assert response.json()["title"] == task1.title


def test_proper_error_responses_for_unauthorized_access(client, setup_test_data):
    """T051: Test proper error responses (401/404) for unauthorized access"""
    user1, user2, task1, task2 = setup_test_data

    # Generate token for user2
    user2_token = create_access_token(data={"sub": str(user2.user_id)})

    # User2 tries to update User1's task - should return 404
    response = client.put(
        f"/api/tasks/{task1.id}",
        json={"title": "Updated title"},
        headers={"Authorization": f"Bearer {user2_token}"}
    )

    assert response.status_code == 404  # Task not found for this user

    # User2 tries to delete User1's task - should return 404
    response = client.delete(
        f"/api/tasks/{task1.id}",
        headers={"Authorization": f"Bearer {user2_token}"}
    )

    assert response.status_code == 404  # Task not found for this user

    # Test with invalid token - should return 401
    response = client.get(
        f"/api/tasks/{task1.id}",
        headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == 401  # Unauthorized
import pytest
from fastapi.testclient import TestClient
from uuid import UUID
from src.models.task import TaskCreate, TaskUpdate


def test_task_lifecycle(client: TestClient):
    """Test the complete task lifecycle: create, read, update, delete"""
    # First, create a user and get their token
    signup_response = client.post(
        "/api/auth/signup",
        json={
            "email": "taskuser@example.com",
            "password": "testpassword123"
        }
    )
    assert signup_response.status_code == 200
    signup_data = signup_response.json()
    token = signup_data["token"]
    user_id = signup_data["user_id"]

    # Add Authorization header for subsequent requests
    headers = {"Authorization": f"Bearer {token}"}

    # Test creating a task
    create_response = client.post(
        "/api/tasks",
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "completed": False
        },
        headers=headers
    )
    assert create_response.status_code == 201
    created_task = create_response.json()
    assert created_task["title"] == "Test Task"
    assert created_task["description"] == "This is a test task"
    assert created_task["completed"] is False
    assert "id" in created_task

    task_id = created_task["id"]

    # Test getting the specific task
    get_task_response = client.get(f"/api/tasks/{task_id}", headers=headers)
    assert get_task_response.status_code == 200
    retrieved_task = get_task_response.json()
    assert retrieved_task["id"] == task_id
    assert retrieved_task["title"] == "Test Task"

    # Test getting all user tasks
    get_tasks_response = client.get("/api/tasks", headers=headers)
    assert get_tasks_response.status_code == 200
    tasks_list = get_tasks_response.json()
    assert len(tasks_list) == 1
    assert tasks_list[0]["id"] == task_id

    # Test updating the task
    update_response = client.put(
        f"/api/tasks/{task_id}",
        json={
            "title": "Updated Task",
            "description": "This is an updated task",
            "completed": True
        },
        headers=headers
    )
    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["title"] == "Updated Task"
    assert updated_task["completed"] is True

    # Test toggling task completion
    toggle_response = client.patch(f"/api/tasks/{task_id}/toggle", headers=headers)
    assert toggle_response.status_code == 200
    toggled_task = toggle_response.json()
    assert toggled_task["completed"] is False  # Should be opposite of what it was

    # Test deleting the task
    delete_response = client.delete(f"/api/tasks/{task_id}", headers=headers)
    assert delete_response.status_code == 204

    # Verify the task is gone
    get_deleted_response = client.get(f"/api/tasks/{task_id}", headers=headers)
    assert get_deleted_response.status_code == 404


def test_task_access_control(client: TestClient):
    """Test that users can only access their own tasks"""
    # Create first user
    user1_signup = client.post(
        "/api/auth/signup",
        json={
            "email": "user1@example.com",
            "password": "password123"
        }
    )
    assert user1_signup.status_code == 200
    user1_data = user1_signup.json()
    user1_token = user1_data["token"]

    # Create second user
    user2_signup = client.post(
        "/api/auth/signup",
        json={
            "email": "user2@example.com",
            "password": "password123"
        }
    )
    assert user2_signup.status_code == 200
    user2_data = user2_signup.json()
    user2_token = user2_data["token"]

    # User 1 creates a task
    headers1 = {"Authorization": f"Bearer {user1_token}"}
    create_response = client.post(
        "/api/tasks",
        json={
            "title": "User 1 Task",
            "description": "This belongs to user 1",
            "completed": False
        },
        headers=headers1
    )
    assert create_response.status_code == 201
    task_data = create_response.json()
    task_id = task_data["id"]

    # User 2 tries to access user 1's task (should fail)
    headers2 = {"Authorization": f"Bearer {user2_token}"}
    get_response = client.get(f"/api/tasks/{task_id}", headers=headers2)
    assert get_response.status_code == 404  # Should return 404, not 403, for security

    # User 2 tries to update user 1's task (should fail)
    update_response = client.put(
        f"/api/tasks/{task_id}",
        json={
            "title": "Hacked Task",
            "completed": True
        },
        headers=headers2
    )
    assert update_response.status_code == 404

    # User 2 tries to delete user 1's task (should fail)
    delete_response = client.delete(f"/api/tasks/{task_id}", headers=headers2)
    assert delete_response.status_code == 404

    # User 1 should still be able to access their own task
    get_response_user1 = client.get(f"/api/tasks/{task_id}", headers=headers1)
    assert get_response_user1.status_code == 200
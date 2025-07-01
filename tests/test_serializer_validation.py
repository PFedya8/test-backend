import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_task_title_validation():
    """Test that empty or whitespace-only titles are rejected."""
    user = User.objects.create_user(username="testuser", password="testpass")
    client = APIClient()

    # Test empty title
    response = client.post(
        "/tasks/", {"title": "", "description": "Test description", "user": user.id}
    )
    assert response.status_code == 400
    assert "title" in response.json()

    # Test whitespace-only title
    response = client.post(
        "/tasks/", {"title": "   ", "description": "Test description", "user": user.id}
    )
    assert response.status_code == 400
    assert "title" in response.json()

    # Test valid title with extra whitespace (should be trimmed)
    response = client.post(
        "/tasks/",
        {
            "title": "  Valid Title  ",
            "description": "Test description",
            "user": user.id,
        },
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Valid Title"


@pytest.mark.django_db
def test_task_description_trimming():
    """Test that description whitespace is properly trimmed."""
    user = User.objects.create_user(username="testuser", password="testpass")
    client = APIClient()

    # Test description with extra whitespace
    response = client.post(
        "/tasks/",
        {
            "title": "Test Task",
            "description": "  Test description with whitespace  ",
            "user": user.id,
        },
    )
    assert response.status_code == 201
    assert response.json()["description"] == "Test description with whitespace"

    # Test empty description
    response = client.post(
        "/tasks/", {"title": "Test Task 2", "description": "   ", "user": user.id}
    )
    assert response.status_code == 201
    assert response.json()["description"] == ""


@pytest.mark.django_db
def test_task_readonly_fields():
    """Test that readonly fields cannot be modified."""
    user = User.objects.create_user(username="testuser", password="testpass")
    client = APIClient()

    # Create a task
    response = client.post(
        "/tasks/",
        {"title": "Test Task", "description": "Test description", "user": user.id},
    )
    assert response.status_code == 201
    task_data = response.json()
    original_created_at = task_data["created_at"]
    task_id = task_data["id"]

    # Try to update readonly fields
    response = client.put(
        f"/tasks/{task_id}/",
        {
            "title": "Updated Task",
            "description": "Updated description",
            "status": "done",
            "user": user.id,
            "created_at": "2020-01-01T00:00:00Z",  # Try to change readonly field
            "updated_at": "2020-01-01T00:00:00Z",  # Try to change readonly field
        },
    )
    assert response.status_code == 200
    updated_data = response.json()

    # Readonly fields should not have changed
    assert updated_data["created_at"] == original_created_at
    assert updated_data["updated_at"] != "2020-01-01T00:00:00Z"

    # Regular fields should have changed
    assert updated_data["title"] == "Updated Task"
    assert updated_data["status"] == "done"

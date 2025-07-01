import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from tasks.models import Task


@pytest.mark.django_db
def test_task_filtering_by_user_id():
    """Test filtering tasks by user_id parameter."""
    user1 = User.objects.create_user(username="user1", password="pass1")
    user2 = User.objects.create_user(username="user2", password="pass2")

    # Create tasks for different users
    Task.objects.create(title="Task 1", user=user1)
    Task.objects.create(title="Task 2", user=user2)
    Task.objects.create(title="Task 3", user=user1)

    client = APIClient()

    # Test filtering by user1
    response = client.get(f"/tasks/?user_id={user1.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for task in data:
        assert task["user"] == user1.id

    # Test filtering by user2
    response = client.get(f"/tasks/?user_id={user2.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["user"] == user2.id


@pytest.mark.django_db
def test_task_filtering_invalid_user_id():
    """Test handling of invalid user_id parameter."""
    user = User.objects.create_user(username="testuser", password="testpass")
    Task.objects.create(title="Task 1", user=user)

    client = APIClient()

    # Test invalid user_id (non-numeric)
    response = client.get("/tasks/?user_id=invalid")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0  # Should return empty result for invalid user_id

    # Test non-existent user_id (but valid number)
    response = client.get("/tasks/?user_id=99999")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


@pytest.mark.django_db
def test_task_pagination():
    """Test pagination with limit and offset parameters."""
    user = User.objects.create_user(username="testuser", password="testpass")

    # Create multiple tasks
    for i in range(5):
        Task.objects.create(title=f"Task {i+1}", user=user)

    client = APIClient()

    # Test limit parameter
    response = client.get("/tasks/?limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

    # Test offset parameter
    response = client.get("/tasks/?offset=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3  # Should return remaining 3 tasks

    # Test limit and offset together
    response = client.get("/tasks/?limit=2&offset=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.django_db
def test_task_pagination_invalid_parameters():
    """Test handling of invalid pagination parameters."""
    user = User.objects.create_user(username="testuser", password="testpass")
    Task.objects.create(title="Task 1", user=user)

    client = APIClient()

    # Test invalid limit (non-numeric)
    response = client.get("/tasks/?limit=invalid")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1  # Should ignore invalid limit and return all

    # Test negative limit
    response = client.get("/tasks/?limit=-1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1  # Should ignore negative limit

    # Test invalid offset (non-numeric)
    response = client.get("/tasks/?offset=invalid")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1  # Should default to offset=0

    # Test negative offset
    response = client.get("/tasks/?offset=-1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1  # Should default to offset=0

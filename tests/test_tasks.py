import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_task_crud():
    user = User.objects.create_user(username="testuser", password="testpass")
    client = APIClient()

    # Create task
    response = client.post(
        "/tasks/",
        {"title": "Test Task", "description": "Test Description", "user": user.id},
    )
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Retrieve task
    response = client.get(f"/tasks/{task_id}/")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

    # Update task
    response = client.put(
        f"/tasks/{task_id}/",
        {
            "title": "Updated Task",
            "description": "Updated Description",
            "status": "done",
            "user": user.id,
        },
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"

    # Delete task
    response = client.delete(f"/tasks/{task_id}/")
    assert response.status_code == 204

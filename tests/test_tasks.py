import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_task_crud():
    user = User.objects.create_user(username='u', password='p')
    client = APIClient()
    resp = client.post('/tasks/', {'title': 't1', 'description': 'd', 'user': user.id})
    assert resp.status_code == 201
    task_id = resp.json()['id']

    resp = client.get(f'/tasks/{task_id}/')
    assert resp.status_code == 200
    assert resp.json()['title'] == 't1'

    resp = client.put(f'/tasks/{task_id}/', {'title': 't2', 'description': 'd2', 'status': 'done', 'user': user.id})
    assert resp.status_code == 200
    assert resp.json()['title'] == 't2'

    resp = client.delete(f'/tasks/{task_id}/')
    assert resp.status_code == 204

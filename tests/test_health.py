import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_healthz():
    client = APIClient()
    resp = client.get('/healthz')
    assert resp.status_code == 200
    assert resp.text == 'alive'


@pytest.mark.django_db
def test_readyz():
    client = APIClient()
    resp = client.get('/readyz')
    assert resp.status_code == 200
    assert resp.json()['status'] == 'ok'

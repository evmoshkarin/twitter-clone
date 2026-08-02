import pytest
from app.models import User


def test_get_own_profile(client):
    headers = {'api-key': 'key1'}
    resp = client.get('/api/users/me', headers=headers)
    assert resp.status_code == 200
    data = resp.json
    assert data['result'] is True
    user = data['user']
    assert user['id'] == 1
    assert user['name'] == 'alice'
    assert 'followers' in user
    assert 'following' in user


def test_get_other_user_profile(client):
    resp = client.get('/api/users/2')
    assert resp.status_code == 200
    data = resp.json
    assert data['result'] is True
    user = data['user']
    assert user['id'] == 2
    assert user['name'] == 'bob'


def test_get_nonexistent_user(client):
    resp = client.get('/api/users/999')
    assert resp.status_code == 404
    data = resp.json
    assert data['result'] is False
    assert data['error_type'] == 'NotFound'

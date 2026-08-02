def test_follow_user(client):
    headers_alice = {'api-key': 'key1'}
    resp = client.post('/api/users/2/follow', headers=headers_alice)
    assert resp.status_code == 200
    assert resp.json['result'] is True

    resp = client.get('/api/users/me', headers=headers_alice)
    user = resp.json['user']
    following_ids = [u['id'] for u in user['following']]
    assert 2 in following_ids


def test_unfollow_user(client):
    headers_alice = {'api-key': 'key1'}
    client.post('/api/users/2/follow', headers=headers_alice)
    resp = client.delete('/api/users/2/follow', headers=headers_alice)
    assert resp.status_code == 200
    assert resp.json['result'] is True

    resp = client.get('/api/users/me', headers=headers_alice)
    user = resp.json['user']
    following_ids = [u['id'] for u in user['following']]
    assert 2 not in following_ids


def test_follow_self(client):
    headers_alice = {'api-key': 'key1'}
    resp = client.post('/api/users/1/follow', headers=headers_alice)
    assert resp.status_code == 200
    assert resp.json['result'] is False
    assert 'error_message' in resp.json

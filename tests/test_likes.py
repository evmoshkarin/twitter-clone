def test_like_tweet(client, app):
    headers_alice = {'api-key': 'key1'}
    tweet_data = {'tweet_data': 'Test tweet for like'}
    resp = client.post('/api/tweets', json=tweet_data, headers=headers_alice)
    tweet_id = resp.json['tweet_id']

    headers_bob = {'api-key': 'key2'}
    resp = client.post(f'/api/tweets/{tweet_id}/likes', headers=headers_bob)
    assert resp.status_code == 200
    assert resp.json['result'] is True

    resp = client.get('/api/tweets', headers=headers_alice)
    tweets = resp.json['tweets']
    found = False
    for t in tweets:
        if t['id'] == tweet_id:
            found = True
            assert len(t['likes']) == 1
            assert t['likes'][0]['user_id'] == 2  # bob
            break
    assert found


def test_unlike_tweet(client, app):
    headers_alice = {'api-key': 'key1'}
    tweet_data = {'tweet_data': 'Another tweet'}
    resp = client.post('/api/tweets', json=tweet_data, headers=headers_alice)
    tweet_id = resp.json['tweet_id']
    headers_bob = {'api-key': 'key2'}
    client.post(f'/api/tweets/{tweet_id}/likes', headers=headers_bob)

    resp = client.delete(f'/api/tweets/{tweet_id}/likes', headers=headers_bob)
    assert resp.status_code == 200
    assert resp.json['result'] is True

    resp = client.get('/api/tweets', headers=headers_alice)
    tweets = resp.json['tweets']
    for t in tweets:
        if t['id'] == tweet_id:
            assert len(t['likes']) == 0
            break


def test_like_nonexistent_tweet(client):
    headers = {'api-key': 'key1'}
    resp = client.post('/api/tweets/999/likes', headers=headers)
    assert resp.status_code == 200
    assert resp.json['result'] is False
    assert 'error_message' in resp.json

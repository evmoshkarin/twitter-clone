def test_create_tweet(client):
    headers = {'api-key': 'key1'}
    data = {'tweet_data': 'Hello world!'}
    resp = client.post('/api/tweets', json=data, headers=headers)
    assert resp.status_code == 200
    assert resp.json['result'] is True
    assert 'tweet_id' in resp.json


def test_get_feed(client):
    headers = {'api-key': 'key1'}
    resp = client.get('/api/tweets', headers=headers)
    assert resp.status_code == 200
    assert resp.json['result'] is True
    assert 'tweets' in resp.json

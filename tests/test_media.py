import io
from app.models import Media


def test_upload_media(client):
    headers = {'api-key': 'key1'}
    data = {
        'file': (io.BytesIO(b'test image content'), 'test.jpg')
    }
    resp = client.post('/api/medias', data=data, headers=headers, content_type='multipart/form-data')
    assert resp.status_code == 200
    json_data = resp.json
    assert json_data['result'] is True
    assert 'media_id' in json_data
    media_id = json_data['media_id']
    media = Media.query.get(media_id)
    assert media is not None
    assert media.file_path.endswith('.jpg')


def test_upload_invalid_file(client):
    headers = {'api-key': 'key1'}
    data = {
        'file': (io.BytesIO(b'not an image'), 'test.txt')
    }
    resp = client.post('/api/medias', data=data, headers=headers, content_type='multipart/form-data')
    assert resp.status_code == 200  # но result = False
    json_data = resp.json
    assert json_data['result'] is False
    assert 'error_message' in json_data


def test_upload_without_file(client):
    headers = {'api-key': 'key1'}
    resp = client.post('/api/medias', headers=headers)
    assert resp.status_code == 400
    json_data = resp.json
    assert json_data['result'] is False

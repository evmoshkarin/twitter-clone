from flask import request, Response
from flask_restx import Namespace, Resource
from app.services.media_service import MediaService
from app.utils.decorators import api_key_required

media_ns = Namespace('media', path='/medias', description='Загрузка и получение медиа')

@media_ns.route('')
class MediaUpload(Resource):
    @api_key_required
    def post(self):
        if 'file' not in request.files:
            return {'result': False, 'error_type': 'BadRequest', 'error_message': 'Файл не отправлен'}, 400
        file = request.files['file']
        media_id = MediaService.save_media(file)
        return {'result': True, 'media_id': media_id}

@media_ns.route('/<int:media_id>')
class MediaGet(Resource):
    def get(self, media_id):
        from app.models import Media
        media = Media.query.get(media_id)
        if not media:
            return {'result': False, 'error_type': 'NotFound', 'error_message': 'Media not found'}, 404
        return Response(media.file_body, mimetype='image/jpeg')

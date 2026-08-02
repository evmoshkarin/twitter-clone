from flask import request
from flask_restx import Namespace, Resource
from app.services.media_service import MediaService
from app.utils.decorators import api_key_required

media_ns = Namespace('media', description='Загрузка медиафайлов')


@media_ns.route('')
class MediaUpload(Resource):
    @api_key_required
    def post(self):
        """Загрузить медиафайл"""
        if 'file' not in request.files:
            return {'result': False, 'error_type': 'BadRequest', 'error_message': 'Файл не отправлен'}, 400
        file = request.files['file']
        media_id = MediaService.save_media(file)
        return {'result': True, 'media_id': media_id}

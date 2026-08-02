from flask import request
from flask_restx import Namespace, Resource
from app.services.like_service import LikeService
from app.utils.decorators import api_key_required

likes_ns = Namespace('tweets', description='Лайки на твитах')


@likes_ns.route('/<int:tweet_id>/likes')
class TweetLike(Resource):
    @api_key_required
    def post(self, tweet_id):
        """Поставить лайк"""
        user = getattr(request, 'current_user')
        LikeService.like_tweet(user.id, tweet_id)
        return {'result': True}

    @api_key_required
    def delete(self, tweet_id):
        """Убрать лайк"""
        user = getattr(request, 'current_user')
        LikeService.unlike_tweet(user.id, tweet_id)
        return {'result': True}

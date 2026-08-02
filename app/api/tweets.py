from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.tweet_service import TweetService
from app.services.user_service import UserService
from app.services.like_service import LikeService
from app.utils.decorators import api_key_required

tweets_ns = Namespace('tweets', description='Операции с твитами')

tweet_model = tweets_ns.model('Tweet', {
    'id': fields.Integer,
    'content': fields.String,
    'attachments': fields.List(fields.String),
    'author': fields.Nested(tweets_ns.model('Author', {
        'id': fields.Integer,
        'name': fields.String
    })),
    'likes': fields.List(fields.Nested(tweets_ns.model('LikeUser', {
        'user_id': fields.Integer,
        'name': fields.String
    })))
})

tweet_create_model = tweets_ns.model('TweetCreate', {
    'tweet_data': fields.String(required=True),
    'tweet_media_ids': fields.List(fields.Integer, required=False)
})

@tweets_ns.route('')
class TweetList(Resource):
    @api_key_required
    def get(self):
        user = getattr(request, 'current_user')
        feed = TweetService.get_feed(user.id)
        return {'result': True, 'tweets': feed}

    @api_key_required
    @tweets_ns.expect(tweet_create_model)
    def post(self):
        data = request.json
        user = getattr(request, 'current_user')
        tweet_id = TweetService.create_tweet(
            user.id,
            data['tweet_data'],
            data.get('tweet_media_ids', [])
        )
        return {'result': True, 'tweet_id': tweet_id}

@tweets_ns.route('/<int:tweet_id>')
class TweetDetail(Resource):
    @api_key_required
    def delete(self, tweet_id):
        user = getattr(request, 'current_user')
        TweetService.delete_tweet(tweet_id, user.id)
        return {'result': True}

@tweets_ns.route('/<int:tweet_id>/likes')
class TweetLike(Resource):
    @api_key_required
    def post(self, tweet_id):
        user = getattr(request, 'current_user')
        LikeService.like_tweet(user.id, tweet_id)
        return {'result': True}

    @api_key_required
    def delete(self, tweet_id):
        user = getattr(request, 'current_user')
        LikeService.unlike_tweet(user.id, tweet_id)
        return {'result': True}

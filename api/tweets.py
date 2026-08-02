from flask import request, current_app
from flask_restx import Namespace, Resource, fields
from app.schemas import tweet_create_model, tweet_model
from app.services.tweet_service import TweetService
from app.services.user_service import UserService
from app.utils.decorators import api_key_required

tweets_ns = Namespace('tweets', description='Операции с твитами')

@tweets_ns.route('')
class TweetList(Resource):
    @api_key_required
    @tweets_ns.marshal_list_with(tweet_model)
    def get(self):
        """Получить ленту твитов"""
        user = getattr(request, 'current_user')
        feed = TweetService.get_feed(user.id)
        return {'result': True, 'tweets': feed}

    @api_key_required
    @tweets_ns.expect(tweet_create_model)
    def post(self):
        """Создать новый твит"""
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
        """Удалить твит"""
        user = getattr(request, 'current_user')
        TweetService.delete_tweet(tweet_id, user.id)
        return {'result': True}

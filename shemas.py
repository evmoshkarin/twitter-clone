from flask_restx import fields
from extensions import api

tweet_model = api.model('Tweet', {
    'id': fields.Integer,
    'content': fields.String,
    'attachments': fields.List(fields.String),
    'author': fields.Nested(api.model('Author', {
        'id': fields.Integer,
        'name': fields.String
    })),
    'likes': fields.List(fields.Nested(api.model('LikeUser', {
        'user_id': fields.Integer,
        'name': fields.String
    })))
})

user_model = api.model('User', {
    'id': fields.Integer,
    'name': fields.String,
    'followers': fields.List(fields.Nested(api.model('Follower', {
        'id': fields.Integer,
        'name': fields.String
    }))),
    'following': fields.List(fields.Nested(api.model('Following', {
        'id': fields.Integer,
        'name': fields.String
    })))
})

tweet_create_model = api.model('TweetCreate', {
    'tweet_data': fields.String(required=True),
    'tweet_media_ids': fields.List(fields.Integer, required=False)
})

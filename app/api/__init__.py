from flask import Blueprint
from flask_restx import Api
from app.api.tweets import tweets_ns
from app.api.users import users_ns
from app.api.media import media_ns

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp, doc='/swagger/')

api.add_namespace(tweets_ns)
api.add_namespace(users_ns)
api.add_namespace(media_ns)

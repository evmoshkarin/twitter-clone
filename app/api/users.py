from flask import request
from flask_restx import Namespace, Resource
from app.services.user_service import UserService
from app.services.follow_service import FollowService
from app.utils.decorators import api_key_required

users_ns = Namespace('users', description='Операции с пользователями')

@users_ns.route('/me')
class UserMe(Resource):
    @api_key_required
    def get(self):
        user = getattr(request, 'current_user')
        profile = UserService.get_user_profile(user.id)
        return {'result': True, 'user': profile}

@users_ns.route('/<int:user_id>')
class UserDetail(Resource):
    def get(self, user_id):
        profile = UserService.get_user_profile(user_id)
        if not profile:
            return {'result': False, 'error_type': 'NotFound', 'error_message': 'Пользователь не найден'}, 404
        return {'result': True, 'user': profile}

@users_ns.route('/<int:user_id>/follow')
class UserFollow(Resource):
    @api_key_required
    def post(self, user_id):
        user = getattr(request, 'current_user')
        FollowService.follow_user(user.id, user_id)
        return {'result': True}

    @api_key_required
    def delete(self, user_id):
        user = getattr(request, 'current_user')
        FollowService.unfollow_user(user.id, user_id)
        return {'result': True}

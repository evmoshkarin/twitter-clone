from functools import wraps
from flask import request, current_app
from app.services.user_service import UserService


def api_key_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('api-key')
        if not api_key:
            return {'result': False, 'error_type': 'Unauthorized',
                    'error_message': 'API key required'}, 401
        user = UserService.get_user_by_api_key(api_key)
        if not user:
            return {'result': False, 'error_type': 'Unauthorized',
                    'error_message': 'Invalid API key'}, 401
        setattr(request, 'current_user', user)
        return f(*args, **kwargs)

    return decorated

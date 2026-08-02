from app.models import User, Follow
from app.extensions import db


class UserService:
    @staticmethod
    def get_user_by_api_key(api_key):
        return User.query.filter_by(api_key=api_key).first()

    @staticmethod
    def get_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def get_user_profile(user_id):
        user = User.query.get(user_id)
        if not user:
            return None
        return {
            'id': user.id,
            'name': user.name,
            'followers': [{'id': f.follower.id, 'name': f.follower.name} for f in user.followers],
            'following': [{'id': f.followed.id, 'name': f.followed.name} for f in user.following]
        }

    @staticmethod
    def follow_user(follower_id, followed_id):
        if follower_id == followed_id:
            raise ValueError("Нельзя подписаться на себя")
        existing = Follow.query.filter_by(follower_id=follower_id, followed_id=followed_id).first()
        if existing:
            raise ValueError("Уже подписан")
        follow = Follow(follower_id=follower_id, followed_id=followed_id)
        db.session.add(follow)
        db.session.commit()
        return True

    @staticmethod
    def unfollow_user(follower_id, followed_id):
        follow = Follow.query.filter_by(follower_id=follower_id, followed_id=followed_id).first()
        if not follow:
            raise ValueError("Подписка не найдена")
        db.session.delete(follow)
        db.session.commit()
        return True

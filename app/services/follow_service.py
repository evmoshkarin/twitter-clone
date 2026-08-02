from app.models import Follow, User
from app.extensions import db


class FollowService:
    @staticmethod
    def follow_user(follower_id: int, followed_id: int) -> bool:
        """
        Подписать пользователя с id follower_id на пользователя с id followed_id.
        Возвращает True в случае успеха, иначе выбрасывает исключение.
        """
        if follower_id == followed_id:
            raise ValueError("Нельзя подписаться на самого себя")

        followed_user = User.query.get(followed_id)
        if not followed_user:
            raise ValueError("Пользователь не найден")

        existing = Follow.query.filter_by(
            follower_id=follower_id,
            followed_id=followed_id
        ).first()
        if existing:
            raise ValueError("Вы уже подписаны на этого пользователя")

        follow = Follow(follower_id=follower_id, followed_id=followed_id)
        db.session.add(follow)
        db.session.commit()
        return True

    @staticmethod
    def unfollow_user(follower_id: int, followed_id: int) -> bool:
        """
        Отписать пользователя follower_id от пользователя followed_id.
        Возвращает True в случае успеха, иначе выбрасывает исключение.
        """
        follow = Follow.query.filter_by(
            follower_id=follower_id,
            followed_id=followed_id
        ).first()
        if not follow:
            raise ValueError("Подписка не найдена")
        db.session.delete(follow)
        db.session.commit()
        return True

from app.models import Like, Tweet
from app.extensions import db

class LikeService:
    @staticmethod
    def like_tweet(user_id, tweet_id):
        tweet = Tweet.query.get(tweet_id)
        if not tweet:
            raise ValueError("Твит не найден")
        existing = Like.query.filter_by(user_id=user_id, tweet_id=tweet_id).first()
        if existing:
            return True  # уже лайкнуто, просто возвращаем успех
        like = Like(user_id=user_id, tweet_id=tweet_id)
        db.session.add(like)
        db.session.commit()
        return True

    @staticmethod
    def unlike_tweet(user_id, tweet_id):
        like = Like.query.filter_by(user_id=user_id, tweet_id=tweet_id).first()
        if not like:
            raise ValueError("Лайк не найден")
        db.session.delete(like)
        db.session.commit()
        return True

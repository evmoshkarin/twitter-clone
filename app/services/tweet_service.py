from app.models import Tweet, Media, Like, User
from app.extensions import db
from sqlalchemy import func, desc

class TweetService:
    @staticmethod
    def create_tweet(author_id, content, media_ids=None):
        tweet = Tweet(content=content, author_id=author_id)
        db.session.add(tweet)
        db.session.flush()

        if media_ids:
            media = Media.query.filter(Media.id.in_(media_ids), Media.tweet_id.is_(None)).all()
            if len(media) != len(media_ids):
                raise ValueError("Некоторые медиафайлы не найдены или уже привязаны")
            for m in media:
                m.tweet_id = tweet.id

        db.session.commit()
        return tweet.id

    # остальные методы без изменений
    @staticmethod
    def delete_tweet(tweet_id, user_id):
        tweet = Tweet.query.get(tweet_id)
        if not tweet:
            raise ValueError("Твит не найден")
        if tweet.author_id != user_id:
            raise PermissionError("Вы не автор этого твита")
        db.session.delete(tweet)
        db.session.commit()
        return True

    @staticmethod
    def get_feed(user_id):
        from app.models import Follow
        followed_ids = [f.followed_id for f in Follow.query.filter_by(follower_id=user_id).all()]
        if not followed_ids:
            return []

        tweets = (
            db.session.query(
                Tweet,
                func.count(Like.id).label('likes_count')
            )
            .outerjoin(Like, Like.tweet_id == Tweet.id)
            .filter(Tweet.author_id.in_(followed_ids))
            .group_by(Tweet.id)
            .order_by(desc('likes_count'), desc(Tweet.created_at))
            .all()
        )

        result = []
        for tweet, likes_count in tweets:
            author = User.query.get(tweet.author_id)
            attachments = [f"/api/medias/{m.id}" for m in tweet.attachments]
            likes = [{'user_id': l.user_id, 'name': l.user.name} for l in tweet.likes]
            result.append({
                'id': tweet.id,
                'content': tweet.content,
                'attachments': attachments,
                'author': {'id': author.id, 'name': author.name},
                'likes': likes
            })
        return result

    @staticmethod
    def get_tweet_by_id(tweet_id):
        return Tweet.query.get(tweet_id)

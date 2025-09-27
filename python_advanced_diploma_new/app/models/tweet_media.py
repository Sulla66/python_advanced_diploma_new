from app import db
from datetime import datetime

class TweetMedia(db.Model):
    __tablename__ = 'tweet_media'

    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'))
    media_id = db.Column(db.Integer, db.ForeignKey('media.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Упростить отношения - временно закомментировать
    # tweet = db.relationship("Tweet", backref="tweet_media")
    # media = db.relationship("Media", backref="tweet_media")

    def __repr__(self):
        return f'<TweetMedia tweet:{self.tweet_id} media:{self.media_id}>'
from app import db
from datetime import datetime

class Media(db.Model):
    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Упростить отношения
    # tweet_associations = db.relationship("TweetMedia", backref="media")

    def __repr__(self):
        return f'<Media {self.filename}>'
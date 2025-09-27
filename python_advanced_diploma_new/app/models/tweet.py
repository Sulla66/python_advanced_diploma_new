from app import db
from datetime import datetime

class Tweet(db.Model):
    __tablename__ = 'tweets'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(280), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Убрать дублирующее отношение
    # author = db.relationship("User", backref="tweets")

    def __repr__(self):
        return f'<Tweet {self.id} by {self.user_id}>'
from routes import db
from datetime import datetime

class Likes(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    liked_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    liked_post = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Like %r>' % self.id
    
    def serialize(self):
        return {
            'id': self.id,
            'liked_by': self.liked_by,
            'liked_post': self.liked_post,
            'created_at': self.created_at
        }
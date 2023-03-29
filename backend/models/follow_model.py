from routes import db
from datetime import datetime


class FollowRequest(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sender_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<FollowRequest %r>' % self.id

    def serialize(self):
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'status': self.status,
            'created_at': self.created_at
        }

from routes import db
from datetime import datetime

# follows = db.Table('follows',
#                    db.Column('follower_id', db.Integer, db.ForeignKey(
#                        'users.id'), primary_key=True),
#                    db.Column('following_id', db.Integer,
#                              db.ForeignKey('users.id'), primary_key=True),
#                    db.Column('created_at', db.DateTime,
#                              default=datetime.utcnow)
#                    )


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    bio = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    blogs = db.relationship('Blogs', backref='author_id', lazy=True)
    profile = db.relationship('UserProfile', backref='user_id', lazy=True)

# # Define the follow relationship
#     following = db.relationship(
#         'Users', secondary=follows,
#         primaryjoin=(follows.c.follower_id == id),
#         secondaryjoin=(follows.c.following_id == id),
#         backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
#     )

#     # Define a method to follow a user
#     def follow(self, user):
#         if not self.is_following(user):
#             self.following.append(user)

#     # Define a method to unfollow a user
#     def unfollow(self, user):
#         if self.is_following(user):
#             self.following.remove(user)

#     # Define a method to check if a user is following another user
#     def is_following(self, user):
#         return self.following.filter(follows.c.following_id == user.id).count() > 0

#     # Define a method to check if a user is followed by another user
#     def is_followed_by(self, user):
#         return self.followers.filter(follows.c.follower_id == user.id).count() > 0

#     # Define a method to serialize the User model to a dictionary
#     def serialize(self):
#         return {
#             'id': self.id,
#             'username': self.username,
#             'email': self.email,
#             'following_count': self.following.count(),
#             'followers_count': self.followers.count()
#         }

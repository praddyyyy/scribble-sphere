from routes import db

class UserProfile(db.Model):
    __tablename__ = 'users_profile'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String(100), nullable=True)
    user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    current_location = db.Column(db.String(50), nullable=True)
    profession = db.Column(db.String(50), nullable=True)
    current_company = db.Column(db.String(50), nullable=True)
    primary_link = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return '<User %r>' % self.user_id
from routes import db

class Bookmarks(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    bookmarked_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bookmarked_post = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)

    def __repr__(self):
        return '<Bookmark %r>' % self.id
    
    def serialize(self):
        return {
            'id': self.id,
            'bookmarked_by': self.bookmarked_by,
            'bookmarked_post': self.bookmarked_post,
        }
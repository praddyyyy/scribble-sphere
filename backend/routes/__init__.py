from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_uploads import UploadSet, IMAGES, configure_uploads

db = SQLAlchemy()
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['UPLOADED_PHOTOS_DEST'] = 'static/images'
photos = UploadSet('photos', IMAGES)
version = "/api/v1"


configure_uploads(app, photos)

# routes imports has to be done here and not at the top of the file to prevent circular imports
from routes import users
from routes import blogs
from routes import user_profile
from routes import follows
from routes import likes
from routes import bookmarks
from models import user_model
from models import blogs_model
from models import user_profile_model
from models import follow_model
from models import likes_model
from models import bookmark_model

# uncomment to override the existing database

with app.app_context():
    db.init_app(app)
    # db.create_all()
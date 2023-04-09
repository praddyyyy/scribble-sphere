import schedule
import time
from models.user_model import Users
from models.likes_model import Likes
from models.blogs_model import Blogs
from routes import app
from datetime import datetime, timedelta

previous_day_5pm = datetime.now().replace(hour=17, minute=0, second=0,
                                          microsecond=0) - timedelta(days=1)
today_5pm = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)


def dailyReport():
    with app.app_context():
        users = Users.query.all()
        for user in users:
            username = user.username
            email = user.email
            likes = Likes.query.filter_by(liked_by=user.id).all()
            blogs = Blogs.query.filter_by(author=user.id).all()
            total_likes = 0
            total_blogs = 0
            for like in likes:
                liked_on = like.created_at
                if previous_day_5pm <= liked_on <= today_5pm:
                    total_likes += 1

            for blog in blogs:
                blog_created_on = blog.created_at
                if previous_day_5pm <= blog_created_on <= today_5pm:
                    total_blogs += 1
            # print(username, email, total_likes, total_blogs)


def Scheduled():

    # schedule.every().day.at("05:00").do(dailyReport)
    schedule.every(5).seconds.do(dailyReport)

    while True:
        schedule.run_pending()
        time.sleep(1)

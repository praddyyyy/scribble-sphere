import schedule
import time
from models.user_model import Users
from models.likes_model import Likes
from models.blogs_model import Blogs
from routes import app
from datetime import datetime, timedelta

from email.message import EmailMessage
import smtplib
import ssl
from dotenv import load_dotenv
import os

load_dotenv()
email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")


previous_day_5pm = datetime.now().replace(hour=17, minute=0, second=0,
                                          microsecond=0) - timedelta(days=1)
today_5pm = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)

def send_email(email, subject, message):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = str(email)
    msg.set_content(message)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_address, email_password)
        server.send_message(msg)


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
            if datetime.now().day == 1:
                monthlyReport()
                continue
            for like in likes:
                liked_on = like.created_at
                if previous_day_5pm <= liked_on <= today_5pm:
                    total_likes += 1

            for blog in blogs:
                blog_created_on = blog.created_at
                if previous_day_5pm <= blog_created_on <= today_5pm:
                    total_blogs += 1

            body = f"Hi {username},\n\nYou have {total_likes} likes and {total_blogs} blogs today.\n\nRegards,\nTeam ScribbleSphere"
            print(body)
            # send_mail(email, "Daily Report", body)
            send_email(email, "Daily Report", body)
            print("Mail Sent")

def monthlyReport():
    with app.app_context():
        users = Users.query.all()
        now = datetime.now()
        for user in users:
            username = user.username
            email = user.email
            likes = Likes.query.filter_by(liked_by=user.id).all()
            blogs = Blogs.query.filter_by(author=user.id).all()
            total_likes = 0
            total_blogs = 0
            for like in likes:
                liked_on = like.created_at
                if now.year == liked_on.year and now.month == liked_on.month:
                    total_likes += 1

            for blog in blogs:
                blog_created_on = blog.created_at
                if now.year == liked_on.year and now.month == liked_on.month:
                    total_blogs += 1
            body = f"Hi {username},\n\nYou have {total_likes} likes and {total_blogs} blogs this month.\n\nRegards,\nTeam ScribbleSphere"
            print(body)
            send_email(email, "Monthly Report", body)
            print("Mail Sent")

def Scheduled():

    schedule.every().day.at("17:00").do(dailyReport)

    while True:
        schedule.run_pending()
        time.sleep(1)

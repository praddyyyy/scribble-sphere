from email.message import EmailMessage
import smtplib
import ssl
from dotenv import load_dotenv
import os

load_dotenv()
email_address = os.getenv("EMAIL_ADDRESS")
email_password = os.getenv("EMAIL_PASSWORD")


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

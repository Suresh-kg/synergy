from email.mime.text import MIMEText
from loder import get_env
import smtplib

EMAIL = get_env("MAIL_USERNAME")
APP_PASSWORD = get_env("MAIL_PASSWORD")

def send_welcome_email(student_name, student_email):

    subject = "Welcome to Synergy Python Course"

    body = f"""
Hello {student_name},

Welcome to Synergy!
...
"""

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL
    msg['To'] = student_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, APP_PASSWORD)

    server.send_message(msg)
    server.quit()

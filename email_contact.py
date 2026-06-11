import smtplib
from email.mime.text import MIMEText
from loder import get_env

EMAIL = get_env("MAIL_USERNAME")
APP_PASSWORD = get_env("MAIL_PASSWORD")

def send_contact_email(
    name,
    email,
    subject,
    message
):

    body = f"""
New Contact Form Submission

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
"""

    msg = MIMEText(body)

    msg['Subject'] = f"Contact Form - {subject}"
    msg['From'] = EMAIL
    msg['To'] = EMAIL

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    server.starttls()

    server.login(
        EMAIL,
        APP_PASSWORD
    )

    server.send_message(msg)

    server.quit()
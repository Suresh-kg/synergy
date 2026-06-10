import smtplib

from email.mime.text import MIMEText


import sqlite3

def get_setting(key):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT value FROM settings WHERE key=?",
        (key,)
    )
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None

EMAIL = get_setting(
    "EMAIL"
)

APP_PASSWORD = get_setting(
    "APP_PASSWORD"
)

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
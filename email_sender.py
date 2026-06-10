from os import name
from email.mime.text import MIMEText
import sqlite3
import smtplib

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
print("EMAIL:", EMAIL)
print("APP_PASSWORD:", APP_PASSWORD)

def send_welcome_email(student_name, student_email):

    subject = "Welcome to Synergy Python Course"
    body = f"""
Hello {student_name},

Welcome to Synergy!

Your registration has been successfully completed.

What you will receive:
✅ Live Python Classes
✅ Weekly Assignments
✅ Hands-on Projects
✅ Certificate of Completion

We will contact you soon with:
- Course Schedule
- Google Meet Link
- WhatsApp Community Link

Thank you for choosing Synergy.

Regards,
Synergy Team
"""

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL
    msg['To'] = student_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    print("EMAIL:", EMAIL)
    print("APP_PASSWORD length:", len(APP_PASSWORD))
    server.login(EMAIL, APP_PASSWORD)

    server.send_message(msg)

    server.quit()
    
if __name__ == "__main__":
    
    name = "Suresh"
    email = "suresh2004krishna@gmail.com"
    
    try:
        send_welcome_email(name, email)
        print("Email sent successfully")

    except Exception as e:
        print("Email Error:", e)
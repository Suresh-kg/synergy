import smtplib
from email.mime.text import MIMEText
import resend
from loder import get_env

resend.api_key = get_env("RESEND_API_KEY")


EMAIL = get_env("MAIL_USERNAME")
APP_PASSWORD = get_env("MAIL_PASSWORD")

def send_contact_email(name,email,subject,message):

    resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": "youradmin@email.com",
        "subject": f"Contact Form: {subject}",
        "text": f"""
Name: {name}
Email: {email}

{message}
"""
    })

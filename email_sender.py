from email.mime.text import MIMEText
import smtplib
import resend
from loder import get_env

resend.api_key = get_env("RESEND_API_KEY")

def send_welcome_email(student_name, student_email):

    resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": student_email,
        "subject": "Welcome to Synergy Python Course",
        "text": f"Hello {student_name}, Welcome to Synergy!"
    })

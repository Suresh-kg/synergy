from os import name
from email.mime.text import MIMEText
from xmlrpc import server

from httpcore import request

from httpcore import request
from loder import get_env
import smtplib



EMAIL = get_env("MAIL_USERNAME")
    
APP_PASSWORD = get_env("MAIL_PASSWORD")



def send_welcome_email(student_name, student_email):

    subject = "Welcome to Synergy Python Course"
    body = f"""
            Hello {student_name},

            Welcome to Synergy!

            Your registration has been successfully completed.

            What you will receive:
            ✅ Live Python Classes
            ✅ Daily Assignments
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
    server.login(EMAIL, APP_PASSWORD)

    server.send_message(msg)

    server.quit()
    
if __name__ == "__main__":
    
    student_name = request.form["name"]
    student_email = request.form["email"]

    send_welcome_email(
        student_name,
        student_email
    )
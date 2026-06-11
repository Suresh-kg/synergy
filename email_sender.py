from resend import Resend
from loder import get_env

client = Resend(
    api_key=get_env("RESEND_API_KEY")
)

def send_welcome_email(student_name, student_email):

    client.emails.send({
        "from": "onboarding@resend.dev",
        "to": [student_email],
        "subject": "Welcome to Synergy Python Course",
        "text": f"""
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
        })

try:

    send_welcome_email(
        name,
        email
    )

    print("Welcome email sent")

except Exception as e:

    print("Email Error:", e)

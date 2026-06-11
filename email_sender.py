import resend
from loder import get_env

resend.api_key = get_env("RESEND_API_KEY")

def send_welcome_email(student_name, student_email):

    params = {
        "from": "onboarding@resend.dev",
        "to": [student_email],
        "subject": "Welcome to Synergy Python Course",
        "html": f"""
        <h2>Welcome {student_name}!</h2>

        <p>Your registration has been completed successfully.</p>

        <ul>
            <li>Live Python Classes</li>
            <li>Daily Assignments</li>
            <li>Hands-on Projects</li>
            <li>Certificate of Completion</li>
        </ul>

        <p>Thank you for choosing Synergy.</p>
        """
    }

    resend.Emails.send(params)

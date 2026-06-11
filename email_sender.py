import resend
from loder import get_env

resend.api_key = get_env("RESEND_API_KEY")

def send_welcome_email(student_name, student_email):

    params = {
        "from": "onboarding@resend.dev",
        "to": [student_email],
        "subject": "Welcome to Synergy Python Course",
        "html": f"""
        <h2>Welcome {student_name}! 🎉</h2>

        <p>Your registration has been completed successfully.</p>

        <h3>What you will receive:</h3>

        <ul>
            <li>✅ Live Python Classes</li>
            <li>✅ Daily Assignments</li>
            <li>✅ Hands-on Projects</li>
            <li>✅ Certificate of Completion</li>
        </ul>

        <p>We will contact you soon with:</p>

        <ul>
            <li>Google Meet Link</li>
            <li>Course Schedule</li>
            <li>WhatsApp Community Link</li>
        </ul>

        <p>Thank you for choosing Synergy.</p>

        <br>

        <strong>Synergy Team</strong>
        """
    }

    resend.Emails.send(params)

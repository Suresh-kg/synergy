from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import os


def generate_certificate(name, student_id):

    os.makedirs("certificates", exist_ok=True)

    filename = os.path.join(
        "certificates",
        f"{name}.pdf"
    )

    c = canvas.Canvas(filename)

    width = 595
    height = 842

    # Outer Border
    c.setStrokeColor(colors.HexColor("#1e3a8a"))
    c.setLineWidth(6)
    c.rect(30, 30, width - 60, height - 60)

    # Inner Border
    c.setLineWidth(2)
    c.rect(45, 45, width - 90, height - 90)

    # Institute Name
    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(colors.HexColor("#1e3a8a"))
    c.drawCentredString(
        width / 2,
        760,
        "SYNERGY"
    )

    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(
        width / 2,
        700,
        "CERTIFICATE OF COMPLETION"
    )

    # Body
    c.setFont("Helvetica", 16)
    c.setFillColor(colors.black)

    c.drawCentredString(
        width / 2,
        630,
        "This is to certify that"
    )

    c.setFont("Helvetica-Bold", 24)

    c.drawCentredString(
        width / 2,
        580,
        name.upper()
    )

    c.setFont("Helvetica", 16)

    c.drawCentredString(
        width / 2,
        530,
        "has successfully completed the"
    )

    c.setFont("Helvetica-Bold", 18)

    c.drawCentredString(
        width / 2,
        490,
        "Python Programming Course"
    )

    # Date
    issue_date = datetime.now().strftime(
        "%d-%m-%Y"
    )

    c.setFont("Helvetica", 12)

    c.drawString(
        80,
        220,
        f"Issue Date: {issue_date}"
    )

    # Certificate ID
    certificate_id = f"SYN{student_id:04d}"

    c.drawString(
        80,
        195,
        f"Certificate ID: {certificate_id}"
    )

    # Signatures
    c.line(80, 120, 220, 120)

    c.drawString(
        100,
        100,
        "Course Instructor"
    )

    c.line(360, 120, 500, 120)

    c.drawString(
        400,
        100,
        "Synergy Director"
    )

    c.save()

    return filename

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    send_file
)

import sqlite3
import pandas as pd
from email_sender import send_welcome_email

from reportlab.pdfgen import canvas
from flask import send_file
from flask import Flask

from datetime import datetime


app = Flask(__name__)
app.secret_key = "synergy_secret_key_2026"
  
@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/register', methods=['POST'])
def register():

    name = request.form['name']
    email = request.form['email']
    college = request.form['college']
    phone = request.form['phone']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO students(name,email,college,phone)
    VALUES(?,?,?,?)
    """,(name,email,college,phone))

    conn.commit()
    conn.close()

    try:
        send_welcome_email(name, email)
        print("Welcome email sent")

    except Exception as e:
        print("Email Error:", e)

    return """
    <h1>Registration Successful!</h1>
    <a href="/">Go Back</a>
    """
    
@app.route('/admin')
def admin():

    if not session.get('admin'):
        return redirect('/login')

    search = request.args.get('search', '')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if search:

        cursor.execute("""
            SELECT *
            FROM students
            WHERE
                name LIKE ?
                OR email LIKE ?
                OR college LIKE ?
                OR phone LIKE ?
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ))

    else:

        cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()
    
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]
    
    cursor.execute("""
    SELECT COUNT(*)
    FROM students
    WHERE payment_status='Paid'
    """)

    paid_students = cursor.fetchone()[0]

    cursor.execute("""
    SELECT COUNT(*)
    FROM students
    WHERE payment_status='Pending'
    """)

    pending_students = cursor.fetchone()[0]
    
    cursor.execute("""
    SELECT SUM(fee_amount)
    FROM students
    WHERE payment_status='Paid'
    """)

    revenue = cursor.fetchone()[0]

    if revenue is None:
        revenue = 0
        
    
    cursor.execute("""
    SELECT COUNT(*)
    FROM students
    WHERE payment_status='Pending Verification'
    """)

    pending_verification = cursor.fetchone()[0]

    conn.close()

    return render_template(
        'admin.html',
        students=students,
        search=search,
        total_students=total_students,
        paid_students=paid_students,
        pending_students=pending_students,
        revenue=revenue,
        pending_verification=pending_verification

    )

@app.route('/delete/<int:id>')
def delete_student(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/admin')   

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "12345":

            session['admin'] = True

            return redirect('/admin')

        return "Invalid Login"

    return render_template('login.html')

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

    
@app.route('/export')
def export_students():

    print("Export route called")

    if not session.get('admin'):
        print("Not logged in")
        return redirect('/login')

    print("Logged in")

    conn = sqlite3.connect('database.db')

    df = pd.read_sql_query(
        "SELECT * FROM students",
        conn
    )

    print(df.head())

    conn.close()

    df.to_excel("students.xlsx", index=False)

    print("Excel file created")

    return send_file(
        "students.xlsx",
        as_attachment=True
    )
  
@app.route('/certificate/<int:id>')
def generate_certificate(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    conn.close()

    if not student:
        return "Student not found"

    student_name = student[0]

    file_name = f"{student_name}_certificate.pdf"

    pdf = canvas.Canvas(file_name)

    pdf.setFont("Helvetica-Bold", 24)

    pdf.drawCentredString(
        300,
        750,
        "CERTIFICATE OF COMPLETION"
    )

    pdf.setFont("Helvetica", 16)

    pdf.drawCentredString(
        300,
        650,
        "This certificate is awarded to"
    )

    pdf.setFont("Helvetica-Bold", 20)

    pdf.drawCentredString(
        300,
        600,
        student_name
    )

    pdf.drawCentredString(
        300,
        550,
        "For successfully completing"
    )

    pdf.drawCentredString(
        300,
        520,
        "Python Programming Course"
    )

    pdf.save()

    return send_file(
        file_name,
        as_attachment=True
    )


@app.route('/mark_paid/<int:id>')
def mark_paid(id):

    if not session.get('admin'):
        return redirect('/login')

    payment_date = datetime.now().strftime("%d-%m-%Y")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET payment_status='Paid',
            payment_date=?
        WHERE id=?
    """, (payment_date, id))

    conn.commit()
    conn.close()

    return redirect('/admin')



@app.route('/courses')
def courses():
    return render_template('courses.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/payment/<int:id>')
def payment(id):

    return render_template(
        'payment.html',
        student_id=id
    )

@app.route('/submit_payment/<int:id>', methods=['POST'])
def submit_payment(id):

    utr = request.form['utr']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET utr=?,
            payment_status='Pending Verification'
        WHERE id=?
    """, (utr, id))

    conn.commit()
    conn.close()

    return """
    <h2>
    Payment Details Submitted Successfully
    </h2>

    <p>
    Your payment is awaiting verification.
    </p>

    <a href='/'>
        Return Home
    </a>
    """

@app.route('/verify_payment/<int:id>')
def verify_payment(id):

    payment_date = datetime.now().strftime("%d-%m-%Y %H:%M")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE students
        SET payment_status='Paid',
            payment_date=?
        WHERE id=?
    """, (payment_date, id))

    conn.commit()
    conn.close()

    return redirect('/admin')

if __name__ == "__main__":
    app.run(debug=True)

from flask import (
    Flask,
    flash,
    render_template,
    request,
    redirect,
    session,
    send_file,
    url_for
)

import os
import sqlite3
import pandas as pd
from email_sender import send_welcome_email

from reportlab.pdfgen import canvas

from datetime import datetime
from email_contact import send_contact_email

from certificate_generator import (
    generate_certificate
)

from loder import get_env

app = Flask(__name__)
app.secret_key = "synergy_secret_key_2026"
  
@app.route('/')
def home_page():
    return render_template('home.html')

# /// Admin Dashboard route ///
    
@app.route('/synergy_dashboard_8x92_admin')
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
        'synergy_dashboard_8x92_admin.html',
        students=students,
        search=search,
        total_students=total_students,
        paid_students=paid_students,
        pending_students=pending_students,
        revenue=revenue,
        pending_verification=pending_verification

    )
    
#$ Login and Logout routes

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "12345":

            session['admin'] = True

            return redirect('/synergy_dashboard_8x92_admin')

        return render_template(
                "login.html",
                error="Invalid usernma or Password"
            )

    return render_template('login.html')

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

@app.route('/login_submit', methods=['POST'])
def login_submit():

    username = request.form['username']
    password = request.form['password']

    admin_user = get_env("ADMIN_USERNAME")
    admin_pass = get_env("ADMIN_PASSWORD")

    if (
        username == admin_user
        and password == admin_pass
    ):

        session['admin'] = True

        return redirect('/synergy_dashboard_8x92_admin')

    return render_template(
        "login.html",
        error="Invalid User or Password"
    )
    
@app.route('/env-test')
def env_test():

    return {
        "admin": get_env("ADMIN_USERNAME"),
        "secret": get_env("SECRET_KEY"),
        "mail": get_env("MAIL_USERNAME")
    }

# Export route to download students data as Excel file
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
    
# Certificate route to generate and download course completion certificate
@app.route(
    '/certificate/<int:id>'
)
def certificate(id):

    conn = sqlite3.connect(
        'database.db'
    )

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        name,
        payment_status
    FROM students
    WHERE id=?
    """, (id,))

    student = cursor.fetchone()

    conn.close()

    if not student:

        return "Student not found"

    if student[1] != "Paid":

        return """
        <h2>
        Certificate available only
        for paid students.
        </h2>
        """

    file_path = generate_certificate(
        student[0],
        id
    )

    return send_file(
        file_path,
        as_attachment=True
    )

# Mark payment as paid (Admin action)
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

    return redirect('/synergy_dashboard_8x92_admin')

# Delete student record (Admin action)
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

    return redirect('/synergy_dashboard_8x92_admin')   


    
# /// Register route for adding new student ///

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register_submit', methods=['POST'])
def register():

    try:

        name = request.form['name']
        email = request.form['email']
        college = request.form['college']
        phone = request.form['phone']
        year = request.form['year']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Check duplicate email
        cursor.execute(
            "SELECT id FROM students WHERE email=?",
            (email,)
        )

        existing = cursor.fetchone()

        if existing:

            conn.close()

            return """
            <h2>Email already registered.</h2>
            <a href='/register'>Go Back</a>
            """

        # Insert student
        cursor.execute("""
        INSERT INTO students(
            name,
            email,
            college,
            phone,
            year,
            course,
            fee_amount
        )
        VALUES(?,?,?,?,?,?,?)
        """,
        (
            name,
            email,
            college,
            phone,
            year,
            "Python Programming",
            299
        ))

        student_id = cursor.lastrowid

        conn.commit()
        conn.close()

        print("Email sending disabled")

        return redirect(
            url_for(
                'payment',
                student_id=student_id
            )
        )

    except Exception as e:

        print("REGISTER ERROR:", e)

        return f"""
        <h2>Registration Error</h2>
        <p>{e}</p>
        <a href="/register">Go Back</a>
        """, 500
        
@app.route('/payment/<int:student_id>')
def payment(student_id):

    return render_template(
        'payment.html',
        student_id=student_id
    )
    
@app.route('/submit_payment/<int:id>', methods=['POST'])
def submit_payment(id):

    utr = request.form.get('utr', '').strip()

    if not utr:
        flash("Please enter a valid UTR/Transaction ID.", "danger")
        return redirect(f"/payment/{id}")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id
    FROM students
    WHERE utr=? AND id != ?
    """, (utr, id))

    existing = cursor.fetchone()

    payment_date = datetime.now().strftime("%d-%m-%Y %H:%M")

    cursor.execute("""
        UPDATE students
        SET payment_status='Paid',
            payment_date=?
        WHERE id=?
    """, (payment_date, id))
    
    if existing:

        conn.close()

        return """
        <h2 style='color:red;'>
        UTR Already Exists
        </h2>

        <p>
        This transaction ID has already been submitted.
        Please check your UTR number.
        </p>

        <a href='javascript:history.back()'>
        Go Back
        </a>
        """

    cursor.execute("""
    UPDATE students
    SET utr=?,
        payment_status='Pending Verification'
    WHERE id=?
    """, (utr, id))

    conn.commit()
    conn.close()

    return redirect(url_for('success', id=id))

@app.route('/success/<int:id>')
def success(id):
    return render_template(
        'success.html',
        student_id=id
    )
    
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

    return redirect('/synergy_dashboard_8x92_admin')



# /// Contact form routes ///

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/contact_submit', methods=['POST'])
def contact_submit():

    print("CONTACT FORM HIT")

    try:

        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO contact_messages(
            name,
            email,
            subject,
            message
        )
        VALUES(?,?,?,?)
        """,
        (
            name,
            email,
            subject,
            message
        ))

        conn.commit()
        conn.close()

        print("Contact message saved successfully")

        # EMAIL DISABLED FOR RENDER
        # send_contact_email(
        #     name,
        #     email,
        #     subject,
        #     message
        # )

        return render_template(
            'contact_success.html'
        )

    except Exception as e:

        print("CONTACT ERROR:", e)

        return f"""
        <h2>Contact Form Error</h2>
        <p>{e}</p>
        <a href="/contact">Go Back</a>
        """, 500
    
@app.route('/messages')
def messages():

    conn = sqlite3.connect(
        'database.db'
    )

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM contact_messages
        ORDER BY id DESC
    """)

    messages = cursor.fetchall()

    conn.close()

    return render_template(
        'messages.html',
        messages=messages
    )

@app.route('/delete_message/<int:id>')
def delete_message(id):

    conn = sqlite3.connect(
        'database.db'
    )

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM contact_messages WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/messages')


# /// Courses route ///

@app.route('/courses')
def courses():
    return render_template('courses.html')

    
    
    
if __name__ == "__main__":
    app.run(debug=True)

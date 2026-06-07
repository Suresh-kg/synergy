import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

try:
    cursor.execute("""
        ALTER TABLE students
        ADD COLUMN payment_status TEXT DEFAULT 'Pending'
    """)
except:
    print("payment_status already exists")

try:
    cursor.execute("""
        ALTER TABLE students
        ADD COLUMN fee_amount INTEGER DEFAULT 499
    """)
except:
    print("fee_amount already exists")

conn.commit()
conn.close()

print("Database Updated")
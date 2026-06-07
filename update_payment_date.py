import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

try:
    cursor.execute("""
        ALTER TABLE students
        ADD COLUMN payment_date TEXT
    """)
except:
    print("payment_date already exists")

conn.commit()
conn.close()

print("Database Updated")
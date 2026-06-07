import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

try:
    cursor.execute("""
        ALTER TABLE students
        ADD COLUMN utr TEXT
    """)
    print("UTR column added")
except:
    print("UTR column already exists")

conn.commit()
conn.close()
import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
               
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,

    college TEXT NOT NULL,
    phone TEXT NOT NULL,

    payment_status TEXT DEFAULT 'Pending',
    fee_amount INTEGER DEFAULT 299,

    payment_date TEXT,

    utr TEXT UNIQUE,

    year TEXT,
    course TEXT
);
               
""")

conn.commit()

print('done')
conn.close()
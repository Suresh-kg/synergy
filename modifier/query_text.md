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

update


import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
UPDATE settings
SET value = 'admin@123'
WHERE key = 'ADMIN_PASSWORD'
""")

conn.commit()

cursor.execute("SELECT * FROM settings")
print(cursor.fetchall())

conn.close()


creating settings

CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);

UPDATE settings
SET APP_PASSWORD = 'hdqe rllp ztvp vnap'
WHERE APP_PASSWORD = 'ecup chox yuuw nefx';

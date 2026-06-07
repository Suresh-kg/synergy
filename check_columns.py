import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(students)")

for col in cursor.fetchall():
    print(col)

conn.close()
import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO settings VALUES
('EMAIL','synergytech.edu@gmail.com')
""")

cursor.execute("""
INSERT INTO settings VALUES
('APP_PASSWORD','')
""")

cursor.execute("""
INSERT INTO settings VALUES
('ADMIN_USERNAME','admin')
""")

cursor.execute("""
INSERT INTO settings VALUES
('ADMIN_PASSWORD','')
""")

conn.commit()   # IMPORTANT

cursor.execute("SELECT * FROM settings")
print(cursor.fetchall())

conn.close()

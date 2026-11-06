import sqlite3

conn = sqlite3.connect("database/internships.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE internships ADD COLUMN duration TEXT")
    conn.commit()
    print("✅ Duration column added successfully.")
except sqlite3.OperationalError as e:
    print(e)

conn.close()
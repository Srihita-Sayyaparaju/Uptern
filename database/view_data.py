import sqlite3

conn = sqlite3.connect("database/internships.db")
cursor = conn.cursor()

cursor.execute("""
SELECT id, title, company, location
FROM internships
LIMIT 10
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
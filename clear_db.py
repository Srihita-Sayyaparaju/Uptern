import sqlite3

conn = sqlite3.connect("database/internships.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM internships")

conn.commit()
conn.close()

print("✅ All internships deleted successfully!")
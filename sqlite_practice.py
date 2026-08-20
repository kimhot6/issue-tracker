import sqlite3

conn = sqlite3.connect('issues.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS issues (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  status TEXT DEFAULT 'open'
)
""")

payload = ('Fix login bug',)
cursor.execute("INSERT INTO issues (title) VALUES (?)", payload)
conn.commit()

issue_id = 1
cursor.execute("SELECT * FROM issues WHERE id = ?", (issue_id,))
row = cursor.fetchone()
print(row)

cursor.close()
conn.close()

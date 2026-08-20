import sqlite3

conn = sqlite3.connect('issues.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS issues (
  id INTEGER PRIMARY KEY AUTOINCREMENT
  title TEXT NOT NULL
  status TEXT DEFAULT 'open'
)
""")

from flask import Flask, request
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('issues.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS issues(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  status TEXT NOT NULL
)
""")

def row_to_issue(row):
  return {
    'id': row[0],
    'title': row[1],
    'status': row[2]
  }

@app.route("/issues")
def issues():
  rows = cursor.execute("SELECT * FROM issues").fetchall()
  issues = [row_to_issue(row) for row in rows]
  return issues

@app.route("/issues", methods=["POST"])
def post_issue():
  data = request.get_json()
  if data.get('title'):
    status = data.get('status', 'open')
    cursor.execute("INSERT INTO issues (title, status) VALUES (?,?)", (data.get('title'), status))
    conn.commit()
    row = cursor.execute("SELECT * FROM issues WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return row_to_issue(row), 201
  return {'error': 'No Title'}, 400

@app.route("/issues/<int:issue_id>")
def get_issue(issue_id):
  row = cursor.execute("SELECT * FROM issues WHERE id = ?", (issue_id,)).fetchone()
  if row:
    return row_to_issue(row)
  return {'error': 'Not Found'}, 404

@app.route('/issues/<int:issue_id>', methods=['DELETE'])
def delete_issue(issue_id):
  if cursor.execute("SELECT * FROM issues WHERE id = ?", (issue_id,)).fetchone():
    cursor.execute("DELETE FROM issues WHERE id = ?", (issue_id,))
    conn.commit()
    return '', 204
  return {'error': 'Not Found'}, 404

@app.route('/issues/<int:issue_id>', methods=['PATCH'])
def patch_issue(issue_id):
  if cursor.execute("SELECT * FROM issues WHERE id = ?", (issue_id,)).fetchone():
    data = request.get_json()
    if 'title' in data:
      cursor.execute("UPDATE issues SET title = ? WHERE id = ?", (data['title'], issue_id))
    if 'status' in data:
      cursor.execute("UPDATE issues SET status = ? WHERE id = ?", (data['status'], issue_id))
    conn.commit()
    row = cursor.execute("SELECT * FROM issues WHERE id = ?", (issue_id,)).fetchone()
    return row_to_issue(row)
  return {'error': 'Not Found'}, 404

if __name__ == "__main__":
  app.run()

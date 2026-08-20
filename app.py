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

@app.route("/issues")
def issues():
  rows = cursor.execute("SELECT * FROM issues").fetchall()
  issues = []
  for row in rows:
    issue = {
      'id': row[0],
      'title': row[1],
      'status': row[2]
    }
    issues.append(issue)
  return issues

@app.route("/issues", methods=["POST"])
def post_issue():
  data = request.get_json()
  if data.get('title'):
    status = data.get('status', 'open')
    cursor.execute("INSERT INTO issues (title, status) VALUES (?,?)", (data.get('title'), status))
    conn.commit()
    row = cursor.execute("SELECT * FROM issues WHERE id = ?", (cursor.lastrowid,)).fetchone()
    issue = {
      'id': row[0],
      'title': row[1],
      'status': row[2]
    }
    return issue, 201
  return {'error': 'No Title'}, 400

@app.route("/issues/<int:issue_id>")
def get_issue(issue_id):
  row = cursor.execute("SELECT * FROM issues WHERE id = ?", (issue_id,)).fetchone()
  if row:
    return {
      'id': row[0],
      'title': row[1],
      'status': row[2]
    }
  return {'error': 'Not Found'}, 404

# @app.route('/issues/<int:issue_id>', methods=['DELETE'])
# def delete_issue(issue_id):
#   for issue in issue_store:
#     if issue['id'] == issue_id:
#       issue_store.remove(issue)
#       return '', 204
#   return {'error': 'Not Found'}, 404

# @app.route('/issues/<int:issue_id>', methods=['PATCH'])
# def patch_issue(issue_id):
#   for issue in issue_store:
#     if issue['id'] == issue_id:
#       data = request.get_json()
#       if 'title' in data:
#         issue['title'] = data['title']
#       if 'status' in data:
#         issue['status'] = data['status']
#       return issue
#   return {'error': 'Not Found'}, 404

if __name__ == "__main__":
  app.run()

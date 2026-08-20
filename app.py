from flask import Flask, request

app = Flask(__name__)

issue_store = []
next_issue_id = 0

@app.route("/health")
def health():
  return {"status":"ok"}

@app.route("/issues")
def issues():
  return issue_store

@app.route("/issues", methods=["POST"])
def post_issue():
  global next_issue_id
  data = request.get_json()
  if data.get('title'):
    issue = {
      'id': next_issue_id,
      'title': data.get('title'),
      'status': data.get('status', 'open')
    }
    issue_store.append(issue)
    next_issue_id += 1
    return issue, 201
  return {'error': 'No Title'}, 400

@app.route("/issues/<int:issue_id>")
def get_issue(issue_id):
  for issue in issue_store:
    if issue['id'] == issue_id:
      return issue
  return {'error': 'Not Found'}, 404

@app.route('/issues/<int:issue_id>', methods=['DELETE'])
def delete_issue(issue_id):
  for issue in issue_store:
    if issue['id'] == issue_id:
      issue_store.remove(issue)
      return '', 204
  return {'error': 'Not Found'}, 404

if __name__ == "__main__":
  app.run()

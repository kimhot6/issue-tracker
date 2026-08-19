from flask import Flask, request

app = Flask(__name__)

issue_store = []
id = 0

@app.route("/health")
def health():
  return {"status":"ok"}

@app.route("/issues")
def issues():
  return issue_store

@app.route("/issues", methods = ["POST"])
def post_issue():
  global id
  data = request.get_json()
  issue = {
    'id': id,
    'title': data.get('title'),
    'status': data.get('status', 'open')
  }
  issue_store.append(issue)
  id += 1
  return issue, 201

if __name__ == "__main__":
  app.run()

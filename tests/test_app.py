from app import app

client = app.test_client()

def test_health():
  response = client.get("/health")
  assert response.status_code == 200
  assert response.json["status"] == "ok"

def test_issues():
  response = client.get("/issues")
  assert response.status_code == 200
  assert response.json == []

def test_post_issue():
  payload = {'title': 'Fix login bug'}
  response = client.post("/issues", json = payload)
  assert response.status_code == 201
  assert response.json['title'] == 'Fix login bug'
  assert response.json['status'] == 'open'
  response_get = client.get('/issues')
  assert response_get.json[0]['title'] == 'Fix login bug'

def test_post_issue_without_title():
  payload = {}
  response = client.post('/issues', json=payload)
  assert response.status_code == 400

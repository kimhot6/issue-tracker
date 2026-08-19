from app import app
import app as ap
import pytest

client = app.test_client()

@pytest.fixture
def restart():
  ap.next_issue_id = 0
  ap.issue_store.clear()

def test_health(restart):
  response = client.get("/health")
  assert response.status_code == 200
  assert response.json["status"] == "ok"

def test_issues(restart):
  response = client.get("/issues")
  assert response.status_code == 200
  assert response.json == []

def test_post_issue(restart):
  payload = {'title': 'Fix login bug'}
  response = client.post("/issues", json = payload)
  assert response.status_code == 201
  assert response.json['title'] == 'Fix login bug'
  assert response.json['status'] == 'open'
  response_get = client.get('/issues')
  assert response_get.json[0]['title'] == 'Fix login bug'

def test_post_issue_without_title(restart):
  payload = {}
  response = client.post('/issues', json=payload)
  assert response.status_code == 400
  assert response.json['error'] == 'No Title'
  assert ap.next_issue_id == 0
  

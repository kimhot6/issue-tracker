import app as app_module
import pytest

client = app_module.app.test_client()

@pytest.fixture
def reset_state():
  app_module.next_issue_id = 0
  app_module.issue_store.clear()

def test_health(reset_state):
  response = client.get("/health")
  assert response.status_code == 200
  assert response.json["status"] == "ok"

def test_issues(reset_state):
  response = client.get("/issues")
  assert response.status_code == 200
  assert response.json == []

def test_post_issue(reset_state):
  payload = {'title': 'Fix login bug'}
  response = client.post("/issues", json = payload)
  assert response.status_code == 201
  assert response.json['title'] == 'Fix login bug'
  assert response.json['status'] == 'open'
  response_get = client.get('/issues')
  assert response_get.json[0]['title'] == 'Fix login bug'

def test_post_issue_without_title(reset_state):
  payload = {}
  response = client.post('/issues', json=payload)
  assert response.status_code == 400
  assert response.json['error'] == 'No Title'
  assert app_module.next_issue_id == 0
  assert app_module.issue_store == []
  

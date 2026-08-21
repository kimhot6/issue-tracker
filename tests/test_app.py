import app as app_module
import pytest, os

client = app_module.app.test_client()

@pytest.fixture
def reset_state():
  app_module.DB_PATH = 'test.db'
  conn = app_module.get_connection()
  cursor = conn.cursor()
  yield
  os.remove('test.db')
  
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
  response = client.get('/issues')
  assert response.json[0]['title'] == 'Fix login bug'

def test_post_issue_without_title(reset_state):
  payload = {}
  response = client.post('/issues', json=payload)
  assert response.status_code == 400
  assert response.json['error'] == 'No Title'
  row_count = reset_state.cursor.execute("SELECT COUNT(*) FROM issues").fetchone()[0]
  assert row_count == 0
  
def test_get_issue(reset_state):
  payload = {'title': 'Fix login bug'}
  response = client.post('/issues', json = payload)
  assert response.status_code == 201
  issue_id = response.json['id']
  response = client.get(f'/issues/{issue_id}')
  assert response.status_code == 200
  assert response.json['title'] == 'Fix login bug'
  response = client.get(f'/issues/{issue_id+999}')
  assert response.status_code == 404
  assert response.json['error'] == 'Not Found'

def test_delete_issue(reset_state):
  payload = {'title': 'Fix login bug'}
  response = client.post('/issues', json = payload)
  assert response.status_code == 201
  assert response.json['title'] == 'Fix login bug'
  issue_id = response.json['id']
  response = client.delete(f'/issues/{issue_id}')
  assert response.status_code == 204
  response = client.get(f'/issues/{issue_id}')
  assert response.status_code == 404
  assert response.json['error'] == 'Not Found'
  row_count = reset_state.cursor.execute("SELECT COUNT(*) FROM issues").fetchone()[0]
  assert row_count == 0
  response = client.delete(f'/issues/{issue_id+999}')
  assert response.status_code == 404
  assert response.json['error'] == 'Not Found'
  
def test_patch_issue(reset_state):
  payload = {'title': 'Fix login bug'}
  response = client.post('/issues', json=payload)
  assert response.status_code == 201
  assert response.json['title'] == 'Fix login bug'
  assert response.json['status'] == 'open'
  issue_id = response.json['id']
  payload = {'status': 'closed'}
  response = client.patch(f'/issues/{issue_id}', json=payload)
  assert response.status_code == 200
  assert response.json['status'] == 'closed'
  assert response.json['title'] == 'Fix login bug'
  response = client.get(f'/issues/{issue_id}')
  assert response.json['status'] == 'closed'
  response = client.patch(f'/issues/{issue_id+999}')
  assert response.status_code == 404

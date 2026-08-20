import app as app_module
import pytest

client = app_module.app.test_client()
conn = app_module.conn
cursor = app_module.conn.cursor()

@pytest.fixture
def reset_state():
  cursor.execute("DELETE FROM issues")
  conn.commit()
  
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
  row_count = cursor.execute("SELECT COUNT(*) FROM issues").fetchone()[0]
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

# def test_delete_issue(reset_state):
#   payload = {'title': 'Fix login bug'}
#   response = client.post('/issues', json = payload)
#   assert response.status_code == 201
#   assert response.json['title'] == 'Fix login bug'
#   response = client.delete('/issues/0')
#   assert response.status_code == 204
#   response = client.get('/issues/0')
#   assert response.status_code == 404
#   assert response.json['error'] == 'Not Found'
#   assert app_module.issue_store == []
  
# def test_patch_issue(reset_state):
#   payload = {'title': 'Fix login bug'}
#   response = client.post('/issues', json=payload)
#   assert response.status_code == 201
#   assert response.json['title'] == 'Fix login bug'
#   assert response.json['status'] == 'open'
#   payload = {'status': 'closed'}
#   response = client.patch('/issues/0', json=payload)
#   assert response.status_code == 200
#   assert response.json['status'] == 'closed'
#   assert response.json['title'] == 'Fix login bug'
#   response = client.get('/issues/0')
#   assert response.json['status'] == 'closed'
#   response = client.patch('/issues/999')
#   assert response.status_code == 404

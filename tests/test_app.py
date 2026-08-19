from app import app

client = app.test_client()

def test_code():
  response = client.get("/health")  
  assert response.status_code == 200

def test_status():
  response = client.get("/health")  
  assert response.json["status"] == "ok"

def test_issues():
  response = client.get("/issues")
  print(response.json)
  print(response.text)
  print(response.data)
  assert response.json == []

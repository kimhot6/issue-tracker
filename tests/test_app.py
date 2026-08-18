import sys
print(sys.path)
from app import app

client = app.test_client()


def test_code():
  response = client.get("/health")  
  assert response.status_code == 200

def test_status():
  response = client.get("/health")  
  assert response.json["status"] == "ok"


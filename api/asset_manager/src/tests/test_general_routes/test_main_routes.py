from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def setup_function():
    print("setting up")

def test_read_main():
    response = client.get("/api/v1/")
    assert response.status_code == 200

def test_get_pong():
    response = client.get("/api/v1/ping")
    assert response.status_code == 200
    assert response.text == '"PONG"'

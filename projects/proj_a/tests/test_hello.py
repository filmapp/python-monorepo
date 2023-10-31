from app.main import app
from fastapi.testclient import TestClient


def test_hello() -> None:
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello, World!"

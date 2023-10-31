from main import app


def test_hello() -> None:
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "Hello, World!"

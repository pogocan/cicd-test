from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    # Update this dictionary to match your NEW message exactly
    assert response.json() == {
        "Status": "Look Ma, no hands!",
        "Version": "2.0-Automatic",
    }

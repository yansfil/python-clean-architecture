from fastapi.testclient import TestClient

from app.entrypoints.main import app


def test_user_create_api():
    client = TestClient(app)
    response = client.post(
        "/users", json={"id": "grab", "name": "hoyeon", "password": "zzang"}
    )

    assert response.status_code == 201
    assert response.json() == {"id": "grab", "name": "hoyeon"}

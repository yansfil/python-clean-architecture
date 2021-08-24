from fastapi.testclient import TestClient

from app.entrypoints.main import app


# TODO: e2e 테스트들은 docker-compose로 빼기
def test_user_create_api():
    client = TestClient(app)
    response = client.post(
        "/users", json={"id": "grab", "name": "hoyeon", "password": "zzang"}
    )

    assert response.status_code == 201
    assert response.json() == {"id": "grab", "name": "hoyeon"}


def test_post_create_api():
    client = TestClient(app)
    user_id, name, password = "grab", "hoyeon", "good"
    title, content = "제목", "내용"

    # 유저 생성 call
    client.post("/users", json={"id": user_id, "name": name, "password": password})
    # 글 생성 call
    response = client.post(
        "/posts",
        json={
            "user_id": user_id,
            "user_password": password,
            "title": title,
            "content": content,
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": "1",
        "user_id": user_id,
        "user_name": name,
        "title": title,
        "content": content,
    }

import pytest

from app.domains.user import Post, User

pytest.mark.usefixtures("mappers")


def test_create_user(session):
    user_id, name, password = "grab", "hoyeon", "zzang"
    user = User(user_id=user_id, name=name, password=password)

    session.add(user)
    session.commit()

    result = session.query(User).filter_by(user_id=user_id, password=password).first()
    assert result == user


def test_create_post(session):
    user_id, name, password = "grab", "hoyeon", "zzang"
    user = User(user_id=user_id, name=name, password=password)
    post = Post(title="hello", content="world")

    user.create_post(post)
    session.add(user)
    session.commit()

    result = session.query(Post).filter_by(user_id=user.id).first()

    assert result.user_id == user.id
    assert result == post

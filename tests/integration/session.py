from app.domains.user import User, Post


def test_create_user(session):
    name, password = "grab", "zzang"
    user = User(name=name, password=password)

    session.add(user)
    session.commit()

    result = session.query(User).filter_by(name=name, password=password).first()
    assert result == user

def test_create_post(session):
    name, password = "grab", "zzang"
    user = User(name=name, password=password)
    post = Post(title="hello", content="world")

    user.create_post(post)
    session.add(user)
    session.commit()

    result = session.query(Post).filter_by(user_id=user.id).first()

    assert result.user_id == user.id
    assert result == post

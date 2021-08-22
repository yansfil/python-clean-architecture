from app.domains.user import Post, User


def test_create_post_domain():
    name, password = "grab", "zzang"
    user = User(name=name, password=password)

    assert len(user.posts) == 0
    assert user.name == name
    assert user.password == password


def test_user_create_post_domain():
    name, password = "grab", "zzang"
    user = User(name=name, password=password)
    post = Post(title="hello", content="world")

    user.create_post(post)

    assert len(user.posts) == 1
    assert user.posts[0] == post

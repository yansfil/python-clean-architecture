import pytest

from app.services import service
from app.services.dto import CreatePostDTO, CreateUserDTO
from app.services.uow import PostUnitOfWork, UserUnitOfWork

pytest.mark.usefixtures("mappers")


def test_create_user(session_factory):
    user_id, name, password = "grab", "hoyeon", "zzang"
    uow = UserUnitOfWork(session_factory=session_factory)

    user = service.create_user(user_id=user_id, name=name, password=password, uow=uow)

    assert user == CreateUserDTO(user_id=user_id, name=name)


def test_find_all_users(session_factory, mock_default_users):
    user_id, name, password = "grab", "hoyeon", "zzang"
    uow = UserUnitOfWork(session_factory=session_factory)

    users = service.find_all_users(uow=uow)
    for idx, user in enumerate(
        users
    ):  # MEMO: 기본적으로 users는 lazy loading이고 uow의 context manager에 의해 session이 close된다. 따라서 posts 접근 시 에러가 발생한다.
        assert user.user_id == mock_default_users[idx].user_id


def test_delete_user_well(session_factory, mock_default_users):
    user_id, name, password = "grab1", "hoyeon", "grab1"
    uow = UserUnitOfWork(session_factory=session_factory)

    result = service.delete_user(user_id=user_id, password=password, uow=uow)
    assert result is True


def test_delete_user_not_found(session_factory, mock_default_users):
    user_id, name, password = "hardy", "hoyeon", "humphrey"
    uow = UserUnitOfWork(session_factory=session_factory)

    with pytest.raises(Exception):
        service.delete_user(user_id=user_id, password=password, uow=uow)


def test_find_all_posts_service(session_factory, mock_default_posts):
    uow = PostUnitOfWork(session_factory=session_factory)

    posts = service.find_all_posts(uow=uow)
    for idx, post in enumerate(posts):
        assert post == mock_default_posts[idx]


def test_find_post_by_id_service(session_factory, mock_default_posts):
    uow = PostUnitOfWork(session_factory=session_factory)

    post = service.find_post_by_id(post_id=1, uow=uow)

    assert post == mock_default_posts[0]


def test_create_post_service(session_factory, mock_default_users):
    user_id, name, password = (
        mock_default_users[0].user_id,
        mock_default_users[0].name,
        mock_default_users[0].password,
    )
    title, content = "제목", "내용"
    uow = UserUnitOfWork(session_factory=session_factory)

    post = service.create_post(
        user_id=user_id, user_password=password, title=title, content=content, uow=uow
    )

    assert post == CreatePostDTO(
        id=post.id, user_id=user_id, user_name=name, title=title, content=content
    )

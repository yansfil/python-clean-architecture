import pytest

from app.services.dto import CreatePostDTO, CreateUserDTO, FindPostDTO
from app.services.service import PostService, UserService
from app.services.uow import PostUnitOfWork, UserUnitOfWork

pytest.mark.usefixtures("mappers")


@pytest.fixture
def user_service(session_factory, mock_default_users):
    uow = UserUnitOfWork(session_factory=session_factory)
    return UserService(uow=uow)


@pytest.fixture
def post_service(session_factory, user_service, mock_default_posts):
    uow = PostUnitOfWork(session_factory=session_factory)
    return PostService(uow=uow, user_service=user_service)


def test_create_user(session_factory, user_service):
    user_id, name, password = "grab", "hoyeon", "zzang"
    user = user_service.create_user(user_id=user_id, name=name, password=password)

    assert user == CreateUserDTO(user_id=user_id, name=name)


def test_find_all_users(session_factory, user_service):

    users = user_service.find_all_users()

    assert [user.user_id for user in users] == ["grab1", "grab2"]


def test_delete_user_well(session_factory, user_service):
    user_id, name, password = "grab1", "hoyeon", "grab1"

    result = user_service.delete_user(user_id=user_id, password=password)
    assert result is True


def test_delete_user_not_found(session_factory, user_service):
    user_id, name, password = "hardy", "hoyeon", "humphrey"

    with pytest.raises(Exception):
        user_service.delete_user(user_id=user_id, password=password)


def test_find_all_posts_service(session_factory, post_service):
    posts = post_service.find_all_posts()

    # default_mock_posts 참고
    assert posts == [
        FindPostDTO(id=1, user_id=1, title="제목1", content="내용1"),
        FindPostDTO(id=2, user_id=2, title="제목2", content="내용2"),
    ]


def test_find_post_by_id_service(session_factory, post_service):
    post = post_service.find_post_by_id(post_id=1)

    assert post == FindPostDTO(id=1, user_id=1, title="제목1", content="내용1")


def test_create_post_service(session_factory, post_service):
    user_id, name, password = "grab1", "hoyeon1", "grab1"

    title, content = "제목", "내용"

    post = post_service.create_post(
        user_id=user_id, user_password=password, title=title, content=content
    )

    assert post == CreatePostDTO(
        user_id=1, id=post.id, user_name=name, title=title, content=content
    )

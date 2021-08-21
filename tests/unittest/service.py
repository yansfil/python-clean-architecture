from app.services import service
from app.services.dto import CreatePostDTO, CreateUserDTO
from app.services.uow import UserUnitOfWork


def test_create_user_service(session_factory):
    user_id, name, password = "grab", "hoyeon", "zzang"
    uow = UserUnitOfWork(session_factory=session_factory)

    user = service.create_user(user_id=user_id, name=name, password=password, uow=uow)

    assert user == CreateUserDTO(user_id=user_id, name=name)


def test_create_post_service(session_factory):
    user_id, name, password, title, content = "grab", "hoyeon", "zzang", "제목", "내용"
    uow = UserUnitOfWork(session_factory=session_factory)

    user = service.create_user(user_id=user_id, password=password, name=name, uow=uow)
    post = service.create_post(
        user_id=user_id, user_password=password, title=title, content=content, uow=uow
    )

    assert post == CreatePostDTO(
        id=post.id, user_id=user_id, user_name=name, title=title, content=content
    )

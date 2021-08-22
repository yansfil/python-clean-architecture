from typing import List

from app.domains.user import Post, User
from app.services.dto import CreatePostDTO, CreateUserDTO
from app.services.uow import AbstractUnitOfWork


def create_user(
    user_id: str, name: str, password: str, uow: AbstractUnitOfWork
) -> CreateUserDTO:
    with uow:
        user = User(user_id=user_id, name=name, password=password)
        uow.users.create(user)
        uow.commit()
    user.password = None
    return CreateUserDTO(user_id=user.user_id, name=user.name)


def find_user_by_id(user_id: str, uow: AbstractUnitOfWork) -> User:
    with uow:
        user = uow.users.find_one_by_id(user_id=user_id)
        if not user:
            raise Exception("해당 유저가 존재하지 않습니다")
        uow.commit()
    return user


def find_all_users(uow: AbstractUnitOfWork) -> List[User]:
    with uow:
        users = uow.users.find_all()
        uow.commit()
    return users


def create_post(
    user_id: str, user_password: str, title: str, content: str, uow: AbstractUnitOfWork
) -> CreatePostDTO:
    with uow:
        user = uow.users.find_one(user_id=user_id, password=user_password)
        if not user:
            raise Exception("해당 유저가 존재하지 않습니다")
        post = user.create_post(Post(title=title, content=content, user_id=user.id))
        uow.commit()
    return CreatePostDTO(
        id=post.id,
        user_id=user.user_id,
        user_name=user.name,
        title=post.title,
        content=post.content,
    )

from typing import List

from app.domains.model import Post, User
from app.services.dto import CreatePostDTO, CreateUserDTO
from app.services.uow import AbstractUnitOfWork


def create_user(
    user_id: str, name: str, password: str, uow: AbstractUnitOfWork
) -> CreateUserDTO:
    with uow:
        user = User(user_id=user_id, name=name, password=password)
        uow.repo.create(user)
        uow.commit()
    user.password = None
    return CreateUserDTO(user_id=user.user_id, name=user.name)


def find_user_by_id(user_id: str, uow: AbstractUnitOfWork) -> User:
    with uow:
        user = uow.repo.find_one_by_id(user_id=user_id)
        if not user:
            raise Exception("해당 유저가 존재하지 않습니다")
        uow.commit()
    return user


def find_all_users(uow: AbstractUnitOfWork) -> List[User]:
    with uow:
        users = uow.repo.find_all()
        uow.commit()
    return users


def delete_user(user_id: str, password: str, uow: AbstractUnitOfWork):
    with uow:
        user = uow.repo.find_one(user_id=user_id, password=password)
        if not user:
            raise Exception("해당 유저가 존재하지 않습니다")
        uow.repo.delete(user)
        uow.commit()
    return True


def find_all_posts(uow: AbstractUnitOfWork) -> List[Post]:
    with uow:
        posts = uow.repo.find_all()
        uow.commit()
    return posts


def find_post_by_id(post_id: int, uow: AbstractUnitOfWork) -> Post:
    with uow:
        post = uow.repo.find_one_by_id(id=post_id)
        if not post:
            raise Exception("해당 포스트가 존재하지 않습니다")
        uow.commit()
    return post


def create_post(
    user_id: str, user_password: str, title: str, content: str, uow: AbstractUnitOfWork
) -> CreatePostDTO:
    with uow:
        user = uow.repo.find_one(user_id=user_id, password=user_password)
        if not user:
            raise Exception("해당 유저가 존재하지 않습니다")
        post = user.add_post(Post(title=title, content=content, user_id=user.id))
        uow.commit()
    return CreatePostDTO(
        id=post.id,
        user_id=user.user_id,
        user_name=user.name,
        title=post.title,
        content=post.content,
    )

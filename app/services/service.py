from typing import List

from app.domains.events import DeleteUserPosts
from app.domains.model import Post, User
from app.services.dto import CreatePostDTO, CreateUserDTO, FindPostDTO
from app.services.messagebus import message_queue
from app.services.uow import PostUnitOfWork, UserUnitOfWork


class UserService:
    def __init__(self, uow: UserUnitOfWork):
        self.uow = uow

    def create_user(self, user_id: str, name: str, password: str) -> CreateUserDTO:
        with self.uow:
            user = User(user_id=user_id, name=name, password=password)
            self.uow.repo.create(user)
            self.uow.commit()
        user.password = None
        return CreateUserDTO(user_id=user.user_id, name=user.name)

    def find_user_by_id(self, user_id: str) -> User:
        with self.uow:
            user = self.uow.repo.find_one_by_id(id=user_id)
            if not user:
                raise Exception("해당 유저가 존재하지 않습니다")
            self.uow.commit()
        return user

    def find_one_by_password(self, user_id: str, password: str) -> User:
        with self.uow:
            user = self.uow.repo.find_one_by_password(
                user_id=user_id, password=password
            )
            if not user:
                raise Exception("해당 유저가 존재하지 않습니다")
            self.uow.commit()
        return user

    def find_all_users(self) -> List[User]:
        with self.uow:
            users = self.uow.repo.find_all()
            self.uow.commit()
        return users

    def delete_user(self, user_id: str, password: str):
        with self.uow:
            user = self.uow.repo.find_one_by_password(
                user_id=user_id, password=password
            )
            if not user:
                raise Exception("해당 유저가 존재하지 않습니다")
            # self.uow.repo.delete(user)
            message_queue.put_nowait(DeleteUserPosts(user_id=user.id))
        return True


class PostService:
    def __init__(self, uow: PostUnitOfWork, user_service: UserService):
        self.uow = uow
        self.user_service = user_service

    def find_all_posts(self) -> List[FindPostDTO]:
        with self.uow:
            posts = self.uow.repo.find_all()
            self.uow.commit()
        return [
            FindPostDTO(
                id=post.id,
                user_id=post.user_id,
                title=post.title,
                content=post.content,
            )
            for post in posts
        ]

    def find_post_by_id(self, post_id: int) -> FindPostDTO:
        with self.uow:
            post = self.uow.repo.find_one_by_id(id=post_id)
            if not post:
                raise Exception("해당 포스트가 존재하지 않습니다")
            self.uow.commit()
        return FindPostDTO(
            id=post.id,
            user_id=post.user_id,
            title=post.title,
            content=post.content,
        )

    def create_post(
        self, user_id: str, user_password: str, title: str, content: str
    ) -> CreatePostDTO:
        with self.uow:
            user = self.user_service.find_one_by_password(
                user_id=user_id, password=user_password
            )
            if not user:
                raise Exception("해당 유저가 존재하지 않습니다")
            post = self.uow.repo.create(
                Post(title=title, content=content, user_id=user.id)
            )
            self.uow.commit()

        return CreatePostDTO(
            id=post.id,
            user_id=user.id,
            user_name=user.name,
            title=post.title,
            content=post.content,
        )

    def delete_post(self, post_id: int, user_id: str, password: str):
        with self.uow:
            user = self.user_service.find_one_by_password(
                user_id=user_id, password=password
            )
            if not user:
                raise Exception("해당 유저가 존재하지 않습니다")
            post = self.uow.repo.find_one_by_id(id=post_id)
            self.uow.repo.delete(post)
            self.uow.commit()
        return True

import abc
from typing import List

from sqlalchemy.orm import Session

from app.domains.model import Post, User


class AbstractRepository(abc.ABC):
    def __init__(self, session: Session):
        self.session = session

    @abc.abstractmethod
    def create(self, model):
        ...

    @abc.abstractmethod
    def find_one_by_id(self, id):
        ...

    @abc.abstractmethod
    def find_all(self):
        ...

    @abc.abstractmethod
    def delete(self, model):
        ...


class UserRepository(AbstractRepository):
    def create(self, user: User):
        self.session.add(user)

    def find_one_by_id(self, id: str) -> User:
        return self.session.query(User).filter_by(user_id=id).first()

    def find_all(self) -> List[User]:
        return self.session.query(User).all()

    def find_one(self, user_id: str, password: str) -> User:
        return (
            self.session.query(User)
            .filter_by(user_id=user_id, password=password)
            .first()
        )

    def delete(self, user: User):
        self.session.delete(user)


class PostRepository(AbstractRepository):
    def create(self, post: Post):
        self.session.add(post)

    def find_one_by_id(self, id: int) -> Post:
        return self.session.query(Post).filter_by(id=id).first()

    def find_one_by_user_id(self, user_id: int) -> Post:
        return self.session.query(Post).filter_by(user_id=user_id).first()

    def find_all(self) -> List[Post]:
        return self.session.query(Post).all()

    def delete(self, post: Post):
        self.session.delete(post)

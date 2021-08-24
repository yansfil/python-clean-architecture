from __future__ import annotations

import abc

from app.adapters.orm import get_session_factory
from app.adapters.repository import PostRepository, UserRepository


class AbstractUnitOfWork(abc.ABC):
    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class UserUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=None):
        if not session_factory:
            session_factory = get_session_factory()
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.repo = UserRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


class PostUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=None):
        if not session_factory:
            session_factory = get_session_factory()
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.repo = PostRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

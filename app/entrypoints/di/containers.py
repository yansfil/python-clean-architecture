from dependency_injector import containers, providers

from app.adapters.orm import get_session_factory
from app.services.uow import PostUnitOfWork, UserUnitOfWork

session_factory = get_session_factory()


class Container(containers.DeclarativeContainer):
    session_factory = providers.Object(session_factory)
    user_uow = providers.Singleton(UserUnitOfWork, session_factory=session_factory)
    post_uow = providers.Singleton(PostUnitOfWork, session_factory=session_factory)
    ...

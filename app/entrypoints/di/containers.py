from dependency_injector import containers, providers

from app.adapters.orm import get_session_factory
from app.services.uow import UserUnitOfWork

session_factory = get_session_factory()


class Container(containers.DeclarativeContainer):
    session_factory = providers.Object(session_factory)
    uow = providers.Singleton(UserUnitOfWork, session_factory=session_factory)
    ...

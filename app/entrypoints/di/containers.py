from dependency_injector import containers, providers

from app.adapters.orm import get_session_factory
from app.entrypoints.event_source.external.external import ExternalEventEmitter
from app.entrypoints.event_source.external.publisher import PubSubPublisher
from app.services.service import PostService, UserService
from app.services.uow import PostUnitOfWork, UserUnitOfWork

session_factory = get_session_factory()


class Container(containers.DeclarativeContainer):
    session_factory = providers.Object(session_factory)
    user_uow = providers.Singleton(UserUnitOfWork, session_factory=session_factory)
    post_uow = providers.Singleton(PostUnitOfWork, session_factory=session_factory)

    user_service = providers.Factory(UserService, uow=user_uow)
    post_service = providers.Factory(
        PostService, uow=post_uow, user_service=user_service
    )
    pubsub_client = providers.Singleton(PubSubPublisher)
    event_emitter = providers.Singleton(ExternalEventEmitter, publisher=pubsub_client)

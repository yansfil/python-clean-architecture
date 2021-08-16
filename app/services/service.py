from app.domains.user import User
from app.services.uow import AbstractUnitOfWork


def create_user(
    user_id: str, name: str, password: str, uow: AbstractUnitOfWork
) -> User:
    with uow:
        user = User(user_id=user_id, name=name, password=password)
        uow.users.create(user)
        uow.commit()
    return user

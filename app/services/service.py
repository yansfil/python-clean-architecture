from app.adapters.repository import UserRepository
from app.domains.user import User


def create_user(
    user_id: str, name: str, password: str, repository: UserRepository
) -> User:
    user = User(user_id=user_id, name=name, password=password)
    repository.create(user)

    return user

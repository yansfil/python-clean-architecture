from app.adapters.repository import UserRepository
from app.domains.user import User
from app.services.service import create_user


def test_create_user_service(session):
    name, password = "grab", "zzang"
    repository = UserRepository(session)

    user = create_user(name=name, password=password, repository=repository)
    session.commit()

    assert isinstance(user, User)
    assert user.name == name

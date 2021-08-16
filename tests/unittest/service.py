from app.domains.user import User
from app.services.service import create_user
from app.services.uow import UserUnitOfWork


def test_create_user_service(session_factory):
    user_id, name, password = "grab", "hoyeon", "zzang"
    uow = UserUnitOfWork(session_factory=session_factory)

    user = create_user(user_id=user_id, name=name, password=password, uow=uow)

    assert isinstance(user, User)
    assert user.name == name

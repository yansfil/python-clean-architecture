from app.domains.user import User
from app.services.uow import UserUnitOfWork


def test_uow_create_user(session_factory, session):
    uow = UserUnitOfWork(session_factory)
    user = User(user_id="grab", name="hoyeon", password="1234")

    with uow:
        uow.users.create(user)
        uow.commit()

    assert session.query(User).filter_by(user_id="grab").first()

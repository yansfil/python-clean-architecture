import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from app.adapters.orm import metadata, start_mappers
from app.domains.user import User


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session_factory(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db, expire_on_commit=False)
    clear_mappers()


@pytest.fixture
def session(session_factory):
    return session_factory()


### Depends on session
@pytest.fixture(scope="function")
def mock_default_users(session):
    mock_users = [
        User(user_id="grab1", password="grab1", name="hoyeon1", posts=[]),
        User(user_id="grab2", password="grab2", name="hoyeon2", posts=[]),
    ]
    for user in mock_users:
        session.add(user)
    session.commit()
    return mock_users

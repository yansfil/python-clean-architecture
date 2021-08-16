import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.adapters import orm
from app.adapters.orm import metadata
from app.domains.user import User


@pytest.fixture(scope="session")
def session():
    orm.start_mappers()
    engine = create_engine(url=f"sqlite:///db?check_same_thread=False")
    metadata.create_all(engine)
    get_session = sessionmaker(bind=engine)
    session = get_session()
    yield session
    session.close()


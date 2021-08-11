from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.adapters import orm
from app.adapters.orm import metadata
from app.domains.user import User


def test_orm():
    sqlite_filepath = "db"
    orm.start_mappers()
    engine = create_engine(url=f"sqlite:///{sqlite_filepath}")
    metadata.create_all(engine)
    get_session = sessionmaker(bind=engine)
    session = get_session()
    user = User(id=1, name="grab", password="grab")
    session.add(user)
    session.commit()
    assert True

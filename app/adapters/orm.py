from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)
from sqlalchemy.orm import mapper, relationship, sessionmaker

from app.config import DB_PATH
from app.domains.user import Post, User

metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", String(15)),
    Column("name", String(10)),
    Column("password", String(15)),
)

posts = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(30)),
    Column("content", String(500)),
    Column("user_id", ForeignKey("users.id")),
)


def start_mappers():
    posts_mapper = mapper(Post, posts)
    users_mapper = mapper(User, users, properties={"posts": relationship(posts_mapper)})


def get_session_factory():
    engine = create_engine(url=f"sqlite:///{DB_PATH}?check_same_thread=False")
    metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    return session_factory

from sqlalchemy import MetaData, Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import mapper, relationship

from app.domains.post import Post
from app.domains.user import User

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(10)),
    Column('password', String(15))
)

posts = Table(
    'posts', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(10)),
    Column('password', String(15)),
    Column('user_id', ForeignKey('users.id'))
)

def start_mappers():
    users_mapper = mapper(User, users)
    posts_mapper = mapper(Post, posts)


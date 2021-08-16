from sqlalchemy import MetaData, Table, Column, String, Integer, ForeignKey
from sqlalchemy.orm import mapper, relationship

from app.domains.user import User, Post

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
    Column('title', String(30)),
    Column('content', String(500)),
    Column('user_id', ForeignKey('users.id'))
)

def start_mappers():
    posts_mapper = mapper(Post, posts)
    users_mapper = mapper(User, users, properties={"posts": relationship(posts_mapper)})


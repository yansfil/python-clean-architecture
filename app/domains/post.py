import sqlite3
from pydantic.main import Model


class Post(Model):
    id: str
    user_id: str
    title: str
    content: str

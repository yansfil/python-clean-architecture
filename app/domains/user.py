import sqlite3
from pydantic.main import Model


class User(Model):
    id: str
    name: str
    password: str

import sqlite3
from dataclasses import dataclass, field
from typing import List, Optional

from pydantic import BaseModel

from app.domains.post import Post


@dataclass
class User:
    id: int
    name: str
    password: str
    posts: Optional[List[Post]] = field(default_factory=list)

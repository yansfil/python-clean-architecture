from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Post:
    title: str
    content: str
    user_id: Optional[int] = None


class User:
    def __init__(self, name: str, password: str, posts: Optional[List[Post]] = []):
        self.name = name
        self.password = password
        self.posts = posts

    def create_post(self, post: Post):
        self.posts.append(post)
        return post


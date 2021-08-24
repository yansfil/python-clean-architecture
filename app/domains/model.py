from typing import List, Optional


class Post:
    def __init__(self, title: str, content: str, user_id: Optional[int] = None):
        self.title = title
        self.content = content
        self.user_id = user_id


class User:
    def __init__(
        self, user_id: str, name: str, password: str, posts: Optional[List[Post]] = []
    ):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.posts = posts

    def add_post(self, post: Post):
        self.posts.append(post)
        return post

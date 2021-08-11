from pydantic import BaseModel


class Post(BaseModel):
    id: str
    user_id: str
    title: str
    content: str

from pydantic import BaseModel


class CreateUserDTO(BaseModel):
    user_id: str
    name: str


class CreatePostDTO(BaseModel):
    id: str
    user_id: str
    user_name: str
    title: str
    content: str

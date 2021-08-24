from pydantic import BaseModel


class CreateUserDTO(BaseModel):
    user_id: str
    name: str


class FindPostDTO(BaseModel):
    id: str
    user_id: str
    title: str
    content: str


class CreatePostDTO(FindPostDTO):
    user_name: str

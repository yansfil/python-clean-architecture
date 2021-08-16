from pydantic import BaseModel


class UserRequest(BaseModel):
    id: str
    name: str
    password: str


class UserResponse(BaseModel):
    id: str
    name: str

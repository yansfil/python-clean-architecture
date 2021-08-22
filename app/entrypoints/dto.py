from typing import List

from pydantic import BaseModel


class UserRequest(BaseModel):
    id: str
    name: str
    password: str


class UserResponse(BaseModel):
    id: str
    name: str


class UserListResponseItem(BaseModel):
    id: str
    name: str


class UserListResponse(BaseModel):
    items: List[UserListResponseItem]


class PostRequest(BaseModel):
    user_id: str
    user_password: str
    title: str
    content: str


class PostResponse(BaseModel):
    user_id: str
    user_name: str
    id: str
    title: str
    content: str

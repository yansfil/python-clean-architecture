from typing import List, Optional

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


class DeleteUserRequest(BaseModel):
    password: str


class CreatePostRequest(BaseModel):
    user_id: str
    user_password: str
    title: str
    content: str


class PostResponse(BaseModel):
    user_id: int
    user_name: Optional[str]
    id: int
    title: str
    content: str


class PostListResponseItem(BaseModel):
    user_id: int
    id: int
    title: str
    content: str


class PostListResponse(BaseModel):
    items: List[PostListResponseItem]

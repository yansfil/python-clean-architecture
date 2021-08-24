from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.entrypoints.di.containers import Container
from app.entrypoints.dto import (
    CreatePostRequest,
    DeleteUserRequest,
    PostListResponse,
    PostListResponseItem,
    PostResponse,
    UserListResponse,
    UserListResponseItem,
    UserRequest,
    UserResponse,
)
from app.services import service
from app.services.service import PostService, UserService

router = APIRouter(prefix="")


@router.get("/users", status_code=200)
@inject
def find_all_users(service: UserService = Depends(Provide[Container.user_service])):
    users = service.find_all_users()
    return UserListResponse(
        items=[UserListResponseItem(id=user.user_id, name=user.name) for user in users]
    )


@router.get("/users/{user_id}", status_code=200)
@inject
def find_user(
    user_id: str, service: UserService = Depends(Provide[Container.user_service])
):
    user = service.find_user_by_id(user_id=user_id)
    return UserResponse(id=user.user_id, name=user.name)


@router.post("/users", status_code=201)
@inject
def create_user(
    user: UserRequest, service: UserService = Depends(Provide[Container.user_service])
):
    user = service.create_user(
        user_id=user.id,
        name=user.name,
        password=user.password,
    )
    return UserResponse(id=user.user_id, name=user.name)


@router.delete("/users/{user_id}", status_code=204)
@inject
def delete_user(
    user_id: str,
    body: DeleteUserRequest,
    service: UserService = Depends(Provide[Container.user_service]),
):
    service.delete_user(user_id=user_id, password=body.password)
    return True


@router.get("/posts", status_code=200)
@inject
def find_all_posts(service: PostService = Depends(Provide[Container.post_service])):
    posts = service.find_all_posts()
    return PostListResponse(
        items=[
            PostListResponseItem(
                user_id=post.user_id, id=post.id, title=post.title, content=post.content
            )
            for post in posts
        ]
    )


@router.get("/posts/{post_id}", status_code=200)
@inject
def find_post(
    post_id: int, service: PostService = Depends(Provide[Container.post_service])
):
    post = service.find_post_by_id(post_id=post_id)
    return PostResponse(
        user_id=post.user_id, id=post.id, title=post.title, content=post.content
    )


@router.post("/posts", status_code=201)
@inject
def create_post(
    post: CreatePostRequest,
    service: PostService = Depends(Provide[Container.post_service]),
):
    post = service.create_post(
        user_id=post.user_id,
        user_password=post.user_password,
        title=post.title,
        content=post.content,
    )
    return PostResponse(
        user_id=post.user_id,
        user_name=post.user_name,
        id=post.id,
        title=post.title,
        content=post.content,
    )

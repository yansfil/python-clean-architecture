import os
import threading

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.domains.events import DeleteUserPosts, SendEmail
from app.entrypoints.di.containers import Container
from app.entrypoints.event_source.external.external import ExternalEventEmitter
from app.entrypoints.fastapi.dto import (
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
from app.services.messagebus import message_queue
from app.services.service import PostService, UserService

router = APIRouter(prefix="")


@router.get("/users", status_code=200)
@inject
async def find_all_users(
    service: UserService = Depends(Provide[Container.user_service]),
):
    print(f"process_id: {os.getpid()}")
    print(f"thread_id: {threading.get_ident()}")
    message_queue.put_nowait(SendEmail(msg="계정이 삭제되었습니다"))
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


@router.delete("/users/{user_id}", status_code=201)
@inject
def delete_user(
    user_id: str,
    body: DeleteUserRequest,
    service: UserService = Depends(Provide[Container.user_service]),
    emitter: ExternalEventEmitter = Depends(Provide[Container.event_emitter]),
):
    service.delete_user(user_id=user_id, password=body.password)
    emitter.emit(DeleteUserPosts(user_id=int(user_id)))  # 외부 비동기 메시지 큐에 이벤트를 보낸다.
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

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.entrypoints.di.containers import Container
from app.entrypoints.dto import (
    CreatePostRequest,
    DeleteUserRequest,
    PostResponse,
    UserListResponse,
    UserListResponseItem,
    UserRequest,
    UserResponse,
)
from app.services import service
from app.services.uow import AbstractUnitOfWork

router = APIRouter(prefix="")


@router.get("/users", status_code=200)
@inject
def find_all_users(uow: AbstractUnitOfWork = Depends(Provide[Container.user_uow])):
    users = service.find_all_users(uow=uow)
    return UserListResponse(
        items=[UserListResponseItem(id=user.user_id, name=user.name) for user in users]
    )


@router.get("/users/{user_id}", status_code=200)
@inject
def find_user(
    user_id: str, uow: AbstractUnitOfWork = Depends(Provide[Container.user_uow])
):
    user = service.find_user_by_id(user_id=user_id, uow=uow)
    return UserResponse(id=user.user_id, name=user.name)


@router.post("/users", status_code=201)
def create_user(
    user: UserRequest, uow: AbstractUnitOfWork = Depends(Provide[Container.user_uow])
):
    user = service.create_user(
        user_id=user.id,
        name=user.name,
        password=user.password,
        uow=uow,
    )
    return UserResponse(id=user.user_id, name=user.name)


@router.delete("/users/{user_id}", status_code=204)
def delete_user(
    user_id: str,
    body: DeleteUserRequest,
    uow: AbstractUnitOfWork = Depends(Provide[Container.user_uow]),
):
    service.delete_user(user_id=user_id, password=body.password, uow=uow)
    return True


@router.post("/posts", status_code=201)
def create_post(
    post: CreatePostRequest,
    uow: AbstractUnitOfWork = Depends(Provide[Container.user_uow]),
):
    post = service.create_post(
        user_id=post.user_id,
        user_password=post.user_password,
        title=post.title,
        content=post.content,
        uow=uow,
    )
    return PostResponse(**post.dict())

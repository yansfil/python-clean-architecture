from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.adapters import orm
from app.adapters.orm import get_session_factory
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
from app.services.uow import UserUnitOfWork

app = FastAPI()
# Database ORM Mapping
orm.start_mappers()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


@app.post("/users", status_code=201)
def create_user(user: UserRequest):
    uow = UserUnitOfWork(get_session_factory())
    user = service.create_user(
        user_id=user.id,
        name=user.name,
        password=user.password,
        uow=uow,
    )
    return UserResponse(id=user.user_id, name=user.name)


@app.get("/users/{user_id}", status_code=200)
def find_user(user_id: str):
    uow = UserUnitOfWork(get_session_factory())
    user = service.find_user_by_id(user_id=user_id, uow=uow)
    return UserResponse(id=user.user_id, name=user.name)


@app.get("/users", status_code=200)
def find_all_users():
    uow = UserUnitOfWork(get_session_factory())
    users = service.find_all_users(uow=uow)
    return UserListResponse(
        items=[UserListResponseItem(id=user.user_id, name=user.name) for user in users]
    )


@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: str, body: DeleteUserRequest):
    uow = UserUnitOfWork(get_session_factory())
    service.delete_user(user_id=user_id, password=body.password, uow=uow)
    return True


@app.post("/posts", status_code=201)
def create_post(post: CreatePostRequest):
    uow = UserUnitOfWork(get_session_factory())
    post = service.create_post(
        user_id=post.user_id,
        user_password=post.user_password,
        title=post.title,
        content=post.content,
        uow=uow,
    )
    return PostResponse(**post.dict())

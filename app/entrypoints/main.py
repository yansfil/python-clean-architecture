from fastapi import FastAPI

from app.adapters import orm
from app.adapters.orm import get_session_factory
from app.entrypoints.dto import PostRequest, PostResponse, UserRequest, UserResponse
from app.services import service
from app.services.uow import UserUnitOfWork

app = FastAPI()
# Database ORM Mapping
orm.start_mappers()


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


@app.post("/posts", status_code=201)
def create_post(post: PostRequest):
    uow = UserUnitOfWork(get_session_factory())
    post = service.create_post(
        user_id=post.user_id,
        user_password=post.user_password,
        title=post.title,
        content=post.content,
        uow=uow,
    )
    return PostResponse(**post.dict())

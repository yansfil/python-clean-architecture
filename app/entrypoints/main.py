from fastapi import FastAPI

from app.adapters import orm
from app.adapters.orm import get_session_factory
from app.adapters.repository import UserRepository
from app.entrypoints.dto.user import UserRequest, UserResponse
from app.services import service

app = FastAPI()
# Database ORM Mapping
orm.start_mappers()


@app.post("/users", status_code=201)
def create_user(user: UserRequest):
    session_factory = get_session_factory()
    with session_factory() as session:
        repository = UserRepository(session)
        user = service.create_user(
            user_id=user.id,
            name=user.name,
            password=user.password,
            repository=repository,
        )
        session.commit()
        return UserResponse(id=user.user_id, name=user.name)

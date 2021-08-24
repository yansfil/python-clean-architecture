import uvicorn
from fastapi import FastAPI

from app.adapters import orm
from app.entrypoints import router
from app.entrypoints.di.containers import Container
from app.entrypoints.handlers import global_exception_handler


def create_app():
    app = FastAPI()

    orm.start_mappers()
    container = Container()
    container.wire(modules=[router])

    app.include_router(router.router)
    app.add_exception_handler(Exception, global_exception_handler)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )

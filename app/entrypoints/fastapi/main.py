import uvicorn
from fastapi import FastAPI

from app.adapters import orm
from app.entrypoints.di.containers import Container
from app.entrypoints.event_source.internal.internal_loop import (
    run_event_loop_background,
)
from app.entrypoints.fastapi import router
from app.entrypoints.fastapi.handlers import global_exception_handler

orm.start_mappers()


def create_app():
    app = FastAPI()
    container = Container()
    container.wire(modules=[router])

    app.include_router(router.router)
    app.add_exception_handler(Exception, global_exception_handler)
    app.add_event_handler("startup", run_event_loop_background)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )

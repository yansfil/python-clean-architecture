from starlette.requests import Request
from starlette.responses import JSONResponse


async def global_exception_handler(_: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )

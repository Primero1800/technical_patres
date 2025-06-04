from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from starlette.staticfiles import StaticFiles

from src.core.settings import settings
from src.core.config import (
    AppConfigurer,
    SwaggerConfigurer,
    DBConfigurer,
    ExceptionHandlerConfigurer,
)
from src.api import router as router_api


@asynccontextmanager
async def lifespan(application: FastAPI):
    # startup
    yield
    # shutdown
    await DBConfigurer.dispose()


app = AppConfigurer.create_app(
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.openapi = AppConfigurer.get_custom_openapi(app)

# ROUTERS

app.include_router(
    router_api,
    prefix=settings.app.API_PREFIX,
)

SwaggerConfigurer.config_swagger(app, settings.app.APP_TITLE)


# uncomment if is need custom exception_handler
ExceptionHandlerConfigurer.config_exception_handler(app)


######################################################################

SwaggerConfigurer.delete_router_tag(app)


# ROUTES


@app.get(
    "/",
    tags=[settings.tags.ROOT_TAG,],
)
async def top(request: Request) -> str:
    return f"top here"


if __name__ == "__main__":
    # uvicorn src.main:app --host 0.0.0.0 --reload
    uvicorn.run(
        app=settings.run.app1.APP_PATH,
        host=settings.run.app1.APP_HOST,
        port=8000,
        reload=settings.run.app1.APP_RELOAD,
    )

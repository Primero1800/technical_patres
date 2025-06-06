import logging

from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse
from pydantic import ValidationError


logger = logging.getLogger(__name__)


class Errors:
    HANDLER_MESSAGE = "Handled by Application Exception Handler"
    DATABASE_ERROR = "Error occurred while changing database data"


class ExceptionHandlerConfigurer:

    simple_exceptions = [
        ValidationError,
        RequestValidationError,
    ]

    @staticmethod
    def add_simple_exception_handler(exc_class, app: FastAPI):
        @app.exception_handler(exc_class)
        async def simple_exception_handler(request, exc: exc_class):
            exc_argument = exc.errors() if hasattr(exc, "errors") else exc
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": Errors.HANDLER_MESSAGE,
                    "detail": jsonable_encoder(exc_argument)
                }
            )

    @staticmethod
    def config_exception_handler(app: FastAPI):

        for simple_exception in ExceptionHandlerConfigurer.simple_exceptions:
            ExceptionHandlerConfigurer.add_simple_exception_handler(
                exc_class=simple_exception,
                app=app
            )

from datetime import datetime

from fastapi import status
from fastapi.responses import ORJSONResponse
from .exceptions import Errors


class Validator:
    @staticmethod
    async def validate_published_at(
            published_at: int,
    ):
        if published_at and published_at > datetime.now().year:
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": Errors.HANDLER_MESSAGE(),
                    "detail": "Published year can't be greater than current year",
                }
            )
        return

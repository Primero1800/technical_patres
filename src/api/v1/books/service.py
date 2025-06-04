import logging
from typing import TYPE_CHECKING, Optional

from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.tools.exceptions import CustomException
from .repository import BookRepository
from .exceptions import Errors
from .validators import Validator
from .schemas import (
    BookCreate,
    BookUpdate,
    BookUpdatePartial,
)

if TYPE_CHECKING:
    from src.core.models import (
        Book,
    )

CLASS = "Book"
_CLASS = "book"


class BookService:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_all(
            self,
            page: Optional[int] = 1,
            size: Optional[int] = 10,
    ):
        repository: BookRepository = BookRepository(
            session=self.session
        )
        return await repository.get_all(
            page=page,
            size=size,
        )

    async def get_all_full(
            self,
            page: Optional[int] = 1,
            size: Optional[int] = 10,
    ):
        repository: BookRepository = BookRepository(
            session=self.session
        )
        return await repository.get_all_full(
            page=page,
            size=size,
        )

    async def get_one(
            self,
            id: int
    ):
        repository: BookRepository = BookRepository(
            session=self.session
        )
        try:
            return await repository.get_one(id=id)
        except CustomException as exc:
            return ORJSONResponse(
                status_code=exc.status_code,
                content={
                    "message": Errors.HANDLER_MESSAGE(),
                    "detail": exc.msg,
                }
            )

    async def get_one_complex(
            self,
            id: int
    ):
        repository: BookRepository = BookRepository(
            session=self.session
        )
        try:
            return await repository.get_one_complex(id=id)
        except CustomException as exc:
            return ORJSONResponse(
                status_code=exc.status_code,
                content={
                    "message": Errors.HANDLER_MESSAGE(),
                    "detail": exc.msg,
                }
            )

    async def create_one(
            self,
            instance: BookCreate,
    ):
        is_valid_published_at_or_exc = await Validator.validate_published_at(
            instance.published_at
        )
        if isinstance(is_valid_published_at_or_exc, ORJSONResponse):
            return is_valid_published_at_or_exc

        repository: BookRepository = BookRepository(
            session=self.session
        )
        try:
            return await repository.create_one(
                instance=instance,
            )
        except CustomException as exc:
            return ORJSONResponse(
                status_code=exc.status_code,
                content={
                    "message": Errors.HANDLER_MESSAGE(),
                    "detail": exc.msg,
                }
            )

    async def delete_one(
            self,
            orm_model: "Book",
    ):
        if orm_model and isinstance(orm_model, ORJSONResponse):
            return orm_model

        repository: BookRepository = BookRepository(
            session=self.session
        )
        try:
            return await repository.delete_one(orm_model=orm_model)
        except CustomException as exc:
            return ORJSONResponse(
                status_code=exc.status_code,
                content={
                    "message": Errors.HANDLER_MESSAGE(),
                    "detail": exc.msg,
                }
            )

    async def edit_one(
            self,
            orm_model: "Book",
            instance: BookUpdate | BookUpdatePartial,
            is_partial: bool = False
    ):
        if orm_model and isinstance(orm_model, ORJSONResponse):
            return orm_model

        is_valid_published_at_or_exc = await Validator.validate_published_at(
            instance.published_at
        )
        if isinstance(is_valid_published_at_or_exc, ORJSONResponse):
            return is_valid_published_at_or_exc

        repository: BookRepository = BookRepository(
            session=self.session
        )

        try:
            return await repository.edit_one(
                orm_model=orm_model,
                instance=instance,
                is_partial=is_partial,
            )
        except CustomException as exc:
            return ORJSONResponse(
                status_code=exc.status_code,
                content={
                    "message": Errors.HANDLER_MESSAGE(),
                    "detail": exc.msg,
                }
            )

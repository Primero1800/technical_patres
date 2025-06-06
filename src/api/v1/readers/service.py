import logging
from typing import TYPE_CHECKING, Optional

from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.tools.exceptions import CustomException
from .repository import ReaderRepository
from .exceptions import Errors
from .serializer import serialize
from .schemas import (
    ReaderCreate,
    ReaderUpdate,
    ReaderUpdatePartial,
)

if TYPE_CHECKING:
    from src.core.models import (
        Reader,
    )

CLASS = "Reader"
_CLASS = "reader"


class ReaderService:
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
        repository: ReaderRepository = ReaderRepository(
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
        repository: ReaderRepository = ReaderRepository(
            session=self.session
        )
        result = await repository.get_all_full(
            page=page,
            size=size,
        )
        return [await serialize(model=item) for item in result]

    async def get_one(
            self,
            id: int
    ):
        repository: ReaderRepository = ReaderRepository(
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
            id: int,
            actual: bool = False,
            to_schema: bool = True
    ):
        repository: ReaderRepository = ReaderRepository(
            session=self.session
        )
        try:
            result = await repository.get_one_complex(
                id=id,
                actual=actual,
            )
        except CustomException as exc:
            return ORJSONResponse(
                status_code=exc.status_code,
                content={
                    "message": Errors.HANDLER_MESSAGE(),
                    "detail": exc.msg,
                }
            )
        if to_schema:
            return await serialize(model=result)
        return result

    async def get_one_full(
            self,
            id: int,
            actual: bool = False,
    ):
        repository: ReaderRepository = ReaderRepository(
            session=self.session
        )
        try:
            return await repository.get_one_full(
                id=id,
                actual=actual,
            )
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
            instance: ReaderCreate,
    ):
        repository: ReaderRepository = ReaderRepository(
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
            orm_model: "Reader",
    ):
        #  Вернет ответ с ошибкой ORJSONResponse, если нет записей в бд по выбранному id
        if orm_model and isinstance(orm_model, ORJSONResponse):
            return orm_model

        repository: ReaderRepository = ReaderRepository(
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
            orm_model: "Reader",
            instance: ReaderUpdate | ReaderUpdatePartial,
            is_partial: bool = False
    ):
        #  Вернет ответ с ошибкой ORJSONResponse, если нет записей в бд по выбранному id
        if orm_model and isinstance(orm_model, ORJSONResponse):
            return orm_model

        repository: ReaderRepository = ReaderRepository(
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

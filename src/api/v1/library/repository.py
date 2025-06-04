import logging
from typing import TYPE_CHECKING

from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.core.models import (
    Book,
    Reader,
    BorrowedBook,
)
from src.tools.exceptions import CustomException
from .exceptions import Errors

if TYPE_CHECKING:
    from .schemas import (
        BorrowedBookCreate,
    )

CLASS = "BorrowedBook"


class LibraryRepository:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def create_one(
            self,
            instance: "BorrowedBookCreate"
    ):
        orm_model = BorrowedBook(**instance.model_dump())
        try:
            self.session.add(orm_model)
            await self.session.commit()
            await self.session.refresh(orm_model)
            self.logger.info("%s %r was successfully created" % (CLASS, orm_model))
            return orm_model
        except IntegrityError as error:
            self.logger.error(f"Error while orm_model creating", exc_info=error)
            raise CustomException(
                msg=Errors.DATABASE_ERROR()
            )

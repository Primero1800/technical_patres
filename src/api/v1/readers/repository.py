import logging

from fastapi import status
from sqlalchemy import select, Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, with_loader_criteria
from typing import TYPE_CHECKING, Union, Optional

from src.core.models import Reader, BorrowedBook
from src.tools.exceptions import CustomException
from .exceptions import Errors

if TYPE_CHECKING:
    from .schemas import (
        ReaderCreate,
        ReaderUpdate,
        ReaderUpdatePartial,
    )

CLASS = "Reader"


class ReaderRepository:
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
        stmt = select(Reader).order_by(Reader.id).offset((page - 1) * size).limit(size)
        result: Result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def get_all_full(
            self,
            page: Optional[int] = 1,
            size: Optional[int] = 10,
    ):
        stmt = (select(Reader).options(joinedload(Reader.borrowed_books))
                .order_by(Reader.id).offset((page - 1) * size).limit(size))
        result: Result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def get_one(
            self,
            id: int
    ):
        orm_model = await self.session.get(Reader, id)
        if not orm_model:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                msg=Errors.NOT_EXISTS_ID(id)
            )
        return orm_model

    async def get_one_full(
            self,
            id: int = None,
            actual: bool = False,
    ):
        stmt = select(Reader).where(Reader.id == id)
        if actual:
            stmt = stmt.options(
                joinedload(Reader.borrowed_books).
                joinedload(BorrowedBook.book),
                with_loader_criteria(BorrowedBook, BorrowedBook.return_date == None)
            )
        else:
            stmt = stmt.options(
                joinedload(Reader.borrowed_books).
                joinedload(BorrowedBook.book)
            )
        result: Result = await self.session.execute(stmt)
        orm_model: Reader | None = result.unique().scalar_one_or_none()

        if not orm_model:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                msg=Errors.NOT_EXISTS_ID(id)
            )
        return orm_model

    async def get_one_complex(
            self,
            id: int = None,
            actual: bool = False,
    ):
        stmt = select(Reader).where(Reader.id == id)
        if actual:
            stmt = stmt.options(
                joinedload(Reader.borrowed_books),
                with_loader_criteria(BorrowedBook, BorrowedBook.return_date == None)
            )
        else:
            stmt = stmt.options(
                joinedload(Reader.borrowed_books)
            )
        result: Result = await self.session.execute(stmt)
        orm_model: Reader | None = result.unique().scalar_one_or_none()

        if not orm_model:
            raise CustomException(
                status_code=status.HTTP_404_NOT_FOUND,
                msg=Errors.NOT_EXISTS_ID(id)
            )
        return orm_model

    async def create_one(
            self,
            instance: "ReaderCreate"
    ):
        orm_model = Reader(**instance.model_dump())
        try:
            self.session.add(orm_model)
            await self.session.commit()
            await self.session.refresh(orm_model)
            self.logger.info("%r was successfully created" % orm_model)
            return orm_model
        except IntegrityError as error:
            self.logger.error(f"Error while orm_model creating", exc_info=error)
            raise CustomException(
                msg=Errors.ALREADY_EXISTS()
            )

    async def delete_one(
            self,
            orm_model: Reader,
    ) -> None:
        try:
            self.logger.info(f"Deleting %r from database" % orm_model)
            await self.session.delete(orm_model)
            await self.session.commit()
        except IntegrityError as exc:
            self.logger.error("Error while deleting data from database", exc_info=exc)
            raise CustomException(
                msg=Errors.DATABASE_ERROR()
            )

    async def edit_one(
            self,
            instance:  Union["ReaderUpdate", "ReaderUpdatePartial"],
            orm_model: Reader,
            is_partial: bool = False
    ):
        for key, val in instance.model_dump(
                exclude_unset=is_partial,
                exclude_none=is_partial,
        ).items():
            setattr(orm_model, key, val)

        self.logger.warning(f"Editing %r in database" % orm_model)
        try:
            await self.session.commit()
            await self.session.refresh(orm_model)
            self.logger.info("%r was successfully edited" % orm_model)
            return orm_model
        except IntegrityError as exc:
            self.logger.error("Error occurred while editing data in database", exc_info=exc)
            raise CustomException(
                msg=Errors.ALREADY_EXISTS()
            )

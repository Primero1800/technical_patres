from typing import TYPE_CHECKING

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import DBConfigurer
from .service import LibraryService
from ..readers.dependencies import get_one_complex_actual as reader_get_one_complex_actual
from ..readers.dependencies import get_one_full_actual as reader_get_one_full_actual
from ..books.dependencies import get_one as book_get_one

if TYPE_CHECKING:
    from src.core.models import (
        Reader,
        Book,
        BorrowedBook,
    )


async def get_one(
        borrow_id: int,
        session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> "BorrowedBook":
    service: LibraryService = LibraryService(
        session=session
    )
    return await service.get_one(borrow_id)


async def get_reader_complex_actual(
    reader_id: int,
    session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> "Reader":
    return await reader_get_one_complex_actual(id=reader_id, session=session)


async def get_reader_full_actual(
    reader_id: int,
    session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> "Reader":
    return await reader_get_one_full_actual(id=reader_id, session=session)


async def get_book(
    book_id: int,
    session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> "Book":
    return await book_get_one(id=book_id, session=session)

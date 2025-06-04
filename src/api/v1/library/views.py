from typing import TYPE_CHECKING

from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import DBConfigurer

from .service import LibraryService
from .schemas import (
    BorrowedBookRead,
    BorrowedBookCreate,
    BorrowedBookExtended,
)
from . import dependencies as deps
from ..books.dependencies import get_one as get_one_book
from ..readers.dependencies import get_one_complex_actual
from ..auth.dependencies import current_user

if TYPE_CHECKING:
    from src.core.models import (
        Book,
        Reader,
        BorrowedBook,
    )


router = APIRouter()


@router.post(
    "/serve",
    dependencies=[Depends(current_user),],
    status_code=status.HTTP_201_CREATED,
    response_model=BorrowedBookRead,
    description="Borrow one item (for librarians only)"
)
async def borrow_one(
        book: "Book" = Depends(get_one_book),
        reader: "Reader" = Depends(get_one_complex_actual),
        session: AsyncSession = Depends(DBConfigurer.session_getter)
):

    service: LibraryService = LibraryService(
        session=session
    )
    return await service.borrow_one(
        book=book,
        reader=reader,
    )


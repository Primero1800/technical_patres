from typing import TYPE_CHECKING

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import DBConfigurer

from .service import LibraryService
from .schemas import (
    BorrowedBookRead,
)
from . import dependencies as deps
from ..auth.dependencies import current_user
from ..books.schemas import BookLibList

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
        book: "Book" = Depends(deps.get_book),
        reader: "Reader" = Depends(deps.get_reader_complex_actual),
        session: AsyncSession = Depends(DBConfigurer.session_getter)
):

    service: LibraryService = LibraryService(
        session=session
    )
    return await service.borrow_one(
        book=book,
        reader=reader,
    )


@router.post(
    "/return",
    dependencies=[Depends(current_user),],
    status_code=status.HTTP_200_OK,
    response_model=BorrowedBookRead,
    description="Turn one item back (for librarians only)"
)
async def return_one(
        borrowed_book: "BorrowedBook" = Depends(deps.get_one),
        session: AsyncSession = Depends(DBConfigurer.session_getter)
):
    service: LibraryService = LibraryService(
        session=session
    )
    return await service.return_one(
        orm_model=borrowed_book,
    )


@router.get(
    "/info/{reader_id}",
    dependencies=[Depends(current_user),],
    status_code=status.HTTP_200_OK,
    response_model=list[BookLibList],
    description="The list of all actual items by user_id (for librarians only)"
)
async def info(
    reader: "Reader" = Depends(deps.get_reader_full_actual),
    session: AsyncSession = Depends(DBConfigurer.session_getter)
):
    service: LibraryService = LibraryService(
        session=session
    )
    return await service.get_actual_info(
        reader=reader
    )

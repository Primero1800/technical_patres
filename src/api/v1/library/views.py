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
    description="Borrow one item (for librarians only)",
    responses={
        201: {
            "content": {
                "application/json": {
                    "examples": {
                        "example1": {
                            "summary": "One book borrowed",
                            "value": {
                                "id": 1,
                                "reader_id": 12,
                                "book_id": 7,
                                "borrow_date": "2022-06-04T17:28:17.170342",
                                "return_date": None,
                            },
                        }
                    }
                }
            }
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "summary": "Violation of business terms",
                        "value": {
                            "message": "Handled by Library exception handler",
                            "detail": "Not enough quantity"
                        }
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {
                        "summary": "User is not authenticated",
                        "value": "Unauthorized"
                    }
                }
            }
        },
        404: {
            "description": "Book or reader not found",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Handled by Books exception handler",
                        "detail": "Book with id=7 not exists",
                    }
                }
            }
        }
    }
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
    description="Turn one item back (for librarians only)",
    responses={
        200: {
            "content": {
                "application/json": {
                    "examples": {
                        "example1": {
                            "summary": "One book returned",
                            "value": {
                                "id": 1,
                                "reader_id": 12,
                                "book_id": 7,
                                "borrow_date": "2022-06-04T17:28:17.170342",
                                "return_date": "2022-07-04T17:28:17.170342",
                            },
                        }
                    }
                }
            }
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "summary": "Violation of business terms",
                        "value": {
                            "message": "Handled by Library exception handler",
                            "detail": "Invalid operation. The item has already been returned"
                        }
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {
                        "summary": "User is not authenticated",
                        "value": "Unauthorized"
                    }
                }
            }
        },
        404: {
            "description": "BorrowedBook instance not found",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Handled by Library exception handler",
                        "detail": "BorrowedBook with id=7 not exists",
                    }
                }
            }
        }
    }
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
    description="The list of all actual items by user_id (for librarians only)",
    responses={
        200: {
            "content": {
                "application/json": {
                    "examples": {
                        "example1": {
                            "summary": "An actual list of books of chosen reader",
                            "value": [
                                {
                                    "id": 1,
                                    "name": "The Three Musketeers",
                                    "author": "A.Dumas",
                                    "published_at": 2000,
                                    "isbn": "978-3-16-148410-0",
                                    "description": "Unknown"
                                },
                                {
                                    "id": 22,
                                    "name": "Gone with the Wind",
                                    "author": "M.Mitchell",
                                    "published_at": 1970,
                                    "isbn": None,
                                    "description": "Classic literature"
                                }
                            ]
                        }
                    }
                }
            }
        },
        401: {
            "description": "Unauthorized",
            "content": {
                "application/json": {
                    "example": {
                        "summary": "User is not authenticated",
                        "value": "Unauthorized"
                    }
                }
            }
        },
        404: {
            "description": "Reader not found",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Handled by Reader exception handler",
                        "detail": "Reader with id=7 not exists",
                    }
                }
            }
        }
    }
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

from typing import TYPE_CHECKING

from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import DBConfigurer
from .schemas import (
    BookShort,
    BookRead,
    BookExtended,
    BookCreate,
    BookUpdate,
    BookUpdatePartial,
)
from .service import BookService
from . import dependencies as deps
from ..auth.dependencies import current_user

if TYPE_CHECKING:
    from src.core.models import (
        Book,
    )


router = APIRouter()


# 1
@router.get(
        "",
        response_model=list[BookShort],
        status_code=status.HTTP_200_OK,
        description="Get the list of the all items",
        responses={
            200: {
                "content": {
                    "application/json": {
                        "examples": {
                            "example1": {
                                "summary": "A list of books",
                                "value": [
                                    {
                                        "name": "The Three Musketeers",
                                        "author": "A.Dumas",
                                        "published_at": 2000,
                                        "isbn": "978-3-16-148410-0",
                                        "description": "Unknown"
                                    },
                                    {
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
            422: {
                "description": "Validation Error",
                "content": {
                    "application/json": {
                        "examples": {
                            "invalid input": {
                                "summary": "Invalid input data",
                                "value": {
                                    "detail": [
                                        {
                                            "loc": ["query", "page"],
                                            "msg": "Input should be greater than 0",
                                            "type": "greater_than"
                                        }
                                    ]
                                }
                            }
                        }
                    }
                }
            },
        }
)
async def get_all(
        page: int = Query(1, gt=0, description="Result list page number, greater than 0"),
        size: int = Query(10, gt=0, description="Result list page size, greater than 0"),
        session: AsyncSession = Depends(DBConfigurer.session_getter)
):
    service: BookService = BookService(
        session=session,
    )
    return await service.get_all(
        page=page,
        size=size,
    )


# 1_1
@router.get(
        "/full",
        dependencies=[Depends(current_user)],
        response_model=list[BookExtended],
        status_code=status.HTTP_200_OK,
        description="Get the list of the all items (for librarians only)",
        responses={
            200: {
                "content": {
                    "application/json": {
                        "examples": {
                            "example1": {
                                "summary": "A list of books",
                                "value": [
                                    {
                                        "id": 1,
                                        "name": "The Three Musketeers",
                                        "author": "A.Dumas",
                                        "published_at": 2000,
                                        "isbn": "978-3-16-148410-0",
                                        "description": "Unknown",
                                        "quantity": 1,
                                        "borrowed_books": [
                                            {
                                                "id": 1,
                                                "book_id": 1,
                                                "reader_id": 18,
                                                "borrow_date": "2022-06-04T17:28:17.170342",
                                                "return_date": None
                                            },
                                            {
                                                "id": 21,
                                                "book_id": 1,
                                                "reader_id": 24,
                                                "borrow_date": "2022-06-04T17:28:17.170342",
                                                "return_date": "2022-09-04T17:28:17.170342"
                                            }
                                        ]
                                    },
                                    {
                                        "id": 2,
                                        "name": "Gone with the Wind",
                                        "author": "M.Mitchell",
                                        "published_at": 1970,
                                        "isbn": None,
                                        "description": "Classic literature",
                                        "quantity": 14,
                                        "borrowed_books": [
                                            {
                                                "id": 1,
                                                "book_id": 1,
                                                "reader_id": 18,
                                                "borrow_date": "2022-06-04T17:28:17.170342",
                                                "return_date": None
                                            },
                                            {
                                                "id": 21,
                                                "book_id": 1,
                                                "reader_id": 24,
                                                "borrow_date": "2022-06-04T17:28:17.170342",
                                                "return_date": "2022-09-04T17:28:17.170342"
                                            }
                                        ]
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
                    "text/plain": {
                        "examples": {
                            "not authenticated": {
                                "summary": "User is not authenticated",
                                "value": "Unauthorized"
                            }
                        }
                    }
                }
            },
            422: {
                "description": "Validation Error",
                "content": {
                    "application/json": {
                        "examples": {
                            "invalid input": {
                                "summary": "Invalid input data",
                                "value": {
                                    "detail": [
                                        {
                                            "loc": ["query", "page"],
                                            "msg": "Input should be greater than 0",
                                            "type": "greater_than"
                                        }
                                    ]
                                }
                            }
                        }
                    }
                }
            },
        }
)
async def get_all(
        page: int = Query(1, gt=0, description="Result list page number, greater than 0"),
        size: int = Query(10, gt=0, description="Result list page size, greater than 0"),
        session: AsyncSession = Depends(DBConfigurer.session_getter)
):
    service: BookService = BookService(
        session=session
    )
    return await service.get_all_full(
        page=page,
        size=size,
    )


# 2
@router.get(
        "/{id}",
        dependencies=[Depends(current_user), ],
        status_code=status.HTTP_200_OK,
        response_model=BookRead,
        description="Get the item by id (for librarians only)",
        responses={
            200: {
                "content": {
                    "application/json": {
                        "examples": {
                            "example1": {
                                "summary": "One simple book",
                                "value": {
                                    "id": 1,
                                    "name": "The Three Musketeers",
                                    "author": "A.Dumas",
                                    "published_at": 2000,
                                    "isbn": "978-3-16-148410-0",
                                    "description": "Unknown",
                                    "quantity": 14
                                },
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
                "description": "Book not found",
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
async def get_one(
        id: int,
        session: AsyncSession = Depends(DBConfigurer.session_getter)
):
    service: BookService = BookService(
        session=session
    )
    return await service.get_one(
        id=id
    )


# 2_1
@router.get(
    "/{id}/full",
    dependencies=[Depends(current_user), ],
    status_code=status.HTTP_200_OK,
    response_model=BookExtended,
    description="Get the item by id with all relations (for librarians only)",
    responses={
        200: {
            "content": {
                "application/json": {
                    "examples": {
                        "example1": {
                            "summary": "One simple book",
                            "value": {
                                "id": 1,
                                "name": "The Three Musketeers",
                                "author": "A.Dumas",
                                "published_at": 2000,
                                "isbn": "978-3-16-148410-0",
                                "description": "Unknown",
                                "quantity": 1,
                                "borrowed_books": [
                                    {
                                        "id": 1,
                                        "book_id": 1,
                                        "reader_id": 18,
                                        "borrow_date": "2022-06-04T17:28:17.170342",
                                        "return_date": None
                                    },
                                    {
                                        "id": 21,
                                        "book_id": 1,
                                        "reader_id": 24,
                                        "borrow_date": "2022-06-04T17:28:17.170342",
                                        "return_date": "2022-09-04T17:28:17.170342"
                                    }
                                ]
                            },
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
            "description": "Book not found",
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
async def get_one_complex(
        id: int,
        session: AsyncSession = Depends(DBConfigurer.session_getter)
):
    service: BookService = BookService(
        session=session
    )
    return await service.get_one_complex(
        id=id
    )


# 3
@router.post(
    "",
    dependencies=[Depends(current_user),],
    status_code=status.HTTP_201_CREATED,
    response_model=BookRead,
    description="Create one item (for librarians only)",
    responses={
        201: {
            "content": {
                "application/json": {
                    "examples": {
                        "example1": {
                            "summary": "One book created",
                            "value": {
                                "id": 1,
                                "name": "The Three Musketeers",
                                "author": "A.Dumas",
                                "published_at": 2000,
                                "isbn": "978-3-16-148410-0",
                                "description": "Unknown",
                                "quantity": 14
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
                        "summary": "Database insertion error",
                        "value": {
                            "message": "Handled by Books exception handler",
                            "detail": "Book already exists"
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
        422: {
            "description": "Invalid JSON-format or data.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Handled by Application Exception Handler",
                        "detail": [
                            {
                                "type": "json_invalid",
                                "loc": ["body", 46],
                                "msg": "JSON decode error",
                                "input": {},
                                "ctx": {
                                    "error": "Expecting property name enclosed in double quotes"
                                }
                        }
                        ]
                    }
                }
            }
        }
    }
)
async def create_one(
        instance: BookCreate,
        session: AsyncSession = Depends(DBConfigurer.session_getter)
):

    service: BookService = BookService(
        session=session
    )
    return await service.create_one(
        instance=instance,
    )


# 4
@router.delete(
    "/{id}",
    dependencies=[Depends(current_user), ],
    status_code=status.HTTP_204_NO_CONTENT,
    description="Delete one item by id (for librarians only)",
    responses={
        204: {
            "description": "Book was deleted",
            "content": "No content"
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "summary": "Database deleting error",
                        "value": {
                            "message": "Handled by Books exception handler",
                            "detail": "Error occurred while changing database data"
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
            "description": "Book not found",
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
async def delete_one(
        orm_model: "Book" = Depends(deps.get_one),
        session: AsyncSession = Depends(DBConfigurer.session_getter),
):
    service: BookService = BookService(
        session=session
    )
    return await service.delete_one(orm_model)


# 5
@router.put(
    "/{id}",
    dependencies=[Depends(current_user),],
    status_code=status.HTTP_200_OK,
    response_model=BookRead,
    description="Edit one item (for librarians only)",
    responses= {
        200: {
            "content": {
                "application/json": {
                    "examples": {
                        "example1": {
                            "summary": "One simple book",
                            "value": {
                                "id": 1,
                                "name": "The Three Musketeers",
                                "author": "A.Dumas",
                                "published_at": 2000,
                                "isbn": "978-3-16-148410-0",
                                "description": "Unknown",
                                "quantity": 14
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
                        "summary": "Database deleting error",
                        "value": {
                            "message": "Handled by Books exception handler",
                            "detail": "Error occurred while changing database data"
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
            "description": "Book not found",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Handled by Books exception handler",
                        "detail": "Book with id=7 not exists",
                    }
                }
            }
        },
        422: {
            "description": "Invalid JSON-format or data.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Handled by Application Exception Handler",
                        "detail": [
                            {
                                "type": "json_invalid",
                                "loc": ["body", 46],
                                "msg": "JSON decode error",
                                "input": {},
                                "ctx": {
                                    "error": "Expecting property name enclosed in double quotes"
                                }
                        }
                        ]
                    }
                }
            }
        }
    }
)
async def edit_one(
        instance: BookUpdate,
        orm_model: "Book" = Depends(deps.get_one),
        session: AsyncSession = Depends(DBConfigurer.session_getter)
):

    service: BookService = BookService(
        session=session
    )
    return await service.edit_one(
        orm_model=orm_model,
        instance=instance,
    )


# 5_1
@router.patch(
    "/{id}",
    dependencies=[Depends(current_user),],
    status_code=status.HTTP_200_OK,
    response_model=BookRead,
    description="Edit item partially (for librarians only)",
    responses={
        200: {
            "content": {
                "application/json": {
                    "examples": {
                        "example1": {
                            "summary": "One simple book",
                            "value": {
                                "id": 1,
                                "name": "The Three Musketeers",
                                "author": "A.Dumas",
                                "published_at": 2000,
                                "isbn": "978-3-16-148410-0",
                                "description": "Unknown",
                                "quantity": 14
                            },
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
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "example": {
                        "summary": "Database deleting error",
                        "value": {
                            "message": "Handled by Books exception handler",
                            "detail": "Error occurred while changing database data"
                        }
                    }
                }
            }
        },
        404: {
            "description": "Book not found",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Handled by Books exception handler",
                        "detail": "Book with id=7 not exists",
                    }
                }
            }
        },
        422: {
            "description": "Invalid JSON-format or data.",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Handled by Application Exception Handler",
                        "detail": [
                            {
                                "type": "json_invalid",
                                "loc": ["body", 46],
                                "msg": "JSON decode error",
                                "input": {},
                                "ctx": {
                                    "error": "Expecting property name enclosed in double quotes"
                                }
                        }
                        ]
                    }
                }
            }
        }
    }
)
async def edit_one_partial(
        instance: BookUpdatePartial,
        orm_model: "Book" = Depends(deps.get_one),
        session: AsyncSession = Depends(DBConfigurer.session_getter)
):

    service: BookService = BookService(
        session=session
    )
    return await service.edit_one(
        orm_model=orm_model,
        instance=instance,
        is_partial=True,
    )

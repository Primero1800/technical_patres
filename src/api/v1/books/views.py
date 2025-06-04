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
        description="Get the list of the all items"
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
        description="Get the list of the all items (for librarians only)"
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
    description="Get the item by id (for librarians only)"
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
    description="Get the item by id with all relations (for librarians only)"
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
    description="Create one item (for librarians only)"
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
    description="Delete one item by id (for librarians only)"
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
    description="Edit one item (for librarians only)"
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
    description="Edit item partially (for librarians only)"
)
async def edit_one(
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

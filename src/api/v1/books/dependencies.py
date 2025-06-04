from typing import TYPE_CHECKING
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import DBConfigurer
from .service import BookService

if TYPE_CHECKING:
    from src.core.models import Book


async def get_one(
    id: int,
    session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> "Book":
    service: BookService = BookService(
        session=session
    )
    return await service.get_one(id=id)
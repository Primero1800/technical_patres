from typing import TYPE_CHECKING
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import DBConfigurer
from .service import ReaderService

if TYPE_CHECKING:
    from src.core.models import Reader


async def get_one(
    id: int,
    session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> "Reader":
    service: ReaderService = ReaderService(
        session=session
    )
    return await service.get_one(id=id)


async def get_one_complex(
    id: int,
    session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> "Reader":
    service: ReaderService = ReaderService(
        session=session
    )
    return await service.get_one_complex(id=id)


async def get_one_complex_actual(
    id: int,
    session: AsyncSession = Depends(DBConfigurer.session_getter)
) -> "Reader":
    service: ReaderService = ReaderService(
        session=session
    )
    return await service.get_one_complex(id=id, actual=True)

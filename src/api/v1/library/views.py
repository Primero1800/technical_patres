from typing import TYPE_CHECKING

from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import DBConfigurer

from .service import LibraryService
from . import dependencies as deps
from ..books.dependencies import get_one as get_one_book
from ..readers.dependencies import get_one_complex as get_one_reader
from ..auth.dependencies import current_user

if TYPE_CHECKING:
    from src.core.models import (
        Book,
        Reader,
        BorrowedBook,
    )


router = APIRouter()


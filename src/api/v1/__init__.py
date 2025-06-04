from fastapi import APIRouter

from .auth import router as auth_router
from .books import router as books_router
from .readers import router as readers_router
from .library import router as library_router

from src.core.settings import settings


router = APIRouter()

router.include_router(
    auth_router,
    prefix=settings.tags.AUTH_PREFIX,
    tags=[settings.tags.AUTH_TAG]
)

router.include_router(
    books_router,
    prefix=settings.tags.BOOKS_PREFIX,
    tags=[settings.tags.BOOKS_TAG]
)

router.include_router(
    readers_router,
    prefix=settings.tags.READERS_PREFIX,
    tags=[settings.tags.READERS_TAG]
)

router.include_router(
    library_router,
    prefix=settings.tags.LIBRARY_PREFIX,
    tags=[settings.tags.LIBRARY_TAG]
)

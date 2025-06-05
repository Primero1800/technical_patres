from typing import Any

from .schemas import (
    ReaderExtended,
)


async def serialize(model: Any) -> ReaderExtended:
    from ..library import serializer as library_serializer
    borrowed_books = await library_serializer.serialize_many(model)
    return ReaderExtended(**model.to_dict(), borrowed_books=borrowed_books)

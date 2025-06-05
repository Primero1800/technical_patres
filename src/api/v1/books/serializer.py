from typing import Any

from .schemas import (
    BookExtended,
)


async def serialize(model: Any) -> BookExtended:
    from ..library import serializer as library_serializer
    borrowed_books = await library_serializer.serialize_many(model)
    return BookExtended(**model.to_dict(), borrowed_books=borrowed_books)

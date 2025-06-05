from typing import TYPE_CHECKING, Union

from .schemas import (
    BorrowedBookRead,
)

if TYPE_CHECKING:
    from src.core.models import (
        BorrowedBook,
        Book,
        Reader
    )


async def serialize(model: "BorrowedBook") -> BorrowedBookRead:
    return BorrowedBookRead.model_validate(model, from_attributes=True)


async def serialize_many(
        model: Union["Book", "Reader"]
):
    bor_books_list = []
    if hasattr(model, "borrowed_books"):
        bor_books_list = [
            await serialize(borrowed_book) for borrowed_book in model.borrowed_books
        ]
    return sorted(bor_books_list, key=lambda x: x.id)

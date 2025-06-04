from datetime import datetime
from typing import Annotated, Any, Optional

from pydantic import BaseModel, ConfigDict, Field

base_borrow_date_field = Annotated[datetime, Field(
    title="Book's borrowed",
)]

base_return_date_field = Annotated[datetime, Field(
    title="Book's turned back",
)]


class BaseBorrowedBook(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pass


class BorrowedBookRead(BaseBorrowedBook):
    id: int
    book_id: int
    reader_id: int
    borrow_date: base_borrow_date_field
    return_date: Optional[base_return_date_field]


class BorrowedBookCreate(BaseBorrowedBook):
    book_id: int
    reader_id: int


class BorrowedBookExtended(BaseBorrowedBook):
    id: int
    book: Any
    reader: Any
    borrow_date: base_borrow_date_field
    return_date: base_return_date_field

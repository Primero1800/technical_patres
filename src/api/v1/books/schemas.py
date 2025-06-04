from typing import Annotated, Optional, Any

from pydantic import BaseModel, ConfigDict, Field, conint

base_name_field = Annotated[str, Field(
    title="Book's name",
)]

base_author_field = Annotated[str, Field(
    title="Book's author"
)]

base_isbn_field = Annotated[str, Field(
    title="Book's ISBN"
)]

base_published_at_field = Annotated[conint(gt=1000), Field(
    title="Book's year of publication"
)]

base_quantity_field = Annotated[conint(ge=0), Field(
    title="Book's quantity available"
)]


class BaseBook(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: base_name_field
    author: base_author_field
    published_at: Optional[base_published_at_field] = None
    isbn: Optional[base_isbn_field] = None


class BookShort(BaseBook):
    pass


class BookRead(BookShort):
    id: int
    quantity: base_quantity_field


class BookCreate(BookShort):
    quantity: Optional[base_quantity_field] = 1


class BookUpdate(BookCreate):
    pass


class BookUpdatePartial(BaseBook):
    name: Optional[base_name_field] = None
    author: Optional[base_author_field] = None
    quantity: Optional[base_quantity_field] = 1


class BookExtended(BookRead):
    borrowed_books: Any

from typing import Annotated, Optional, Any

from pydantic import BaseModel, ConfigDict, Field, EmailStr

base_name_field = Annotated[str, Field(
    title="Reader's name",
)]

base_email_field = Annotated[EmailStr, Field(
    title="Reader's email"
)]


class BaseReader(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: base_name_field
    email: base_email_field


class ReaderRead(BaseReader):
    id: int


class ReaderCreate(BaseReader):
    pass


class ReaderUpdate(ReaderCreate):
    pass


class ReaderUpdatePartial(BaseReader):
    name: Optional[base_name_field] = None
    email: Optional[base_email_field] = None


class ReaderExtended(ReaderRead):
    borrowed_books: Any

from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base
from src.core.models.mixins import IDIntPkMixin

if TYPE_CHECKING:
    from src.core.models import (
        BorrowedBook,
    )


class Reader(IDIntPkMixin, Base):
    name: Mapped[str] = mapped_column(
        String,
    )
    email: Mapped[EmailStr] = mapped_column(
        String,
        unique=True,
    )
    borrowed_books: Mapped[list["BorrowedBook"]] = relationship(
        "BorrowedBook",
        back_populates="reader",
        cascade="all, delete",
    )

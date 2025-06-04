from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base
from src.core.models.mixins import IDIntPkMixin

if TYPE_CHECKING:
    from src.core.models import (
        BorrowedBook,
    )


class Book(IDIntPkMixin, Base):
    __table_args__ = (
        CheckConstraint("quantity >= 0", name="check_quantity_min_value"),
        CheckConstraint("published_at >= 1000", name="check_published_at_min_value"),
    )

    name: Mapped[str] = mapped_column(
        String,
    )
    author: Mapped[str] = mapped_column(
        String,
    )
    published_at: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
        default=None,
        server_default=None,
    )
    isbn: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=True,
        default=None,
        server_default=None,
    )
    quantity: Mapped[int] = mapped_column(
        Integer,
        default=1,
        server_default='1',
    )
    borrowed_books: Mapped[list["BorrowedBook"]] = relationship(
        "BorrowedBook",
        back_populates="book",
        cascade="all, delete",
    )

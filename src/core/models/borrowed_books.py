from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.config import DBConfigurer
from src.core.models import Base
from src.core.models.mixins import IDIntPkMixin

if TYPE_CHECKING:
    from src.core.models import (
        Book,
        Reader,
    )


class BorrowedBook(IDIntPkMixin, Base):
    book_id: Mapped[int] = mapped_column(
        ForeignKey(f"{DBConfigurer.utils.camel2snake("Book")}.id", ondelete="CASCADE"),
        nullable=False,
    )
    book: Mapped['Book'] = relationship(
        'Book',
        back_populates='borrowed_books',
    )
    reader_id: Mapped[int] = mapped_column(
        ForeignKey(f"{DBConfigurer.utils.camel2snake("Reader")}.id", ondelete="CASCADE"),
        nullable=False,
    )
    reader: Mapped['Reader'] = relationship(
        'Reader',
        back_populates='borrowed_books',
    )

    borrow_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        server_default=func.now()
    )
    return_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        default=None,
        server_default=None,
    )

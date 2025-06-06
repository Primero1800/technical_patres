import logging

from datetime import datetime
from fastapi import status
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import TYPE_CHECKING

from src.core.settings import settings
from src.tools.exceptions import CustomException
from .repository import LibraryRepository
from .exceptions import Errors
from .schemas import BorrowedBookCreate
from ..books.schemas import BookUpdatePartial
from ..books.service import BookService

if TYPE_CHECKING:
    from src.core.models import (
        Reader,
        Book,
        BorrowedBook,
    )

CLASS = "Library"
_CLASS = "library"


class LibraryService:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session
        self.logger = logging.getLogger(__name__)

    async def get_one(
            self,
            id: int
    ):
        repository: LibraryRepository = LibraryRepository(
            session=self.session
        )
        try:
            return await repository.get_one(id=id)
        except CustomException as exc:
            return ORJSONResponse(
                status_code=exc.status_code,
                content={
                    "message": Errors.HANDLER_MESSAGE(),
                    "detail": exc.msg,
                }
            )

    async def borrow_one(
            self,
            book: "Book",
            reader: "Reader"
    ):
        #  Вернет ответ с ошибкой ORJSONResponse, если нет записей в бд по выбранным reader_id и book_id
        if isinstance(book, ORJSONResponse):
            return book
        if isinstance(reader, ORJSONResponse):
            return reader

        #  Вернет ответ с ошибкой ORJSONResponse, если количество выбранной позиции < 1
        if book.quantity < 1:
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": Errors.HANDLER_MESSAGE(),
                    "detail": Errors.NOT_ENOUGH_QUANTITY(),
                }
            )

        #  Вернет ответ с ошибкой ORJSONResponse, если превышен лимит на количество книг "на руках"
        # В borrowed_books по выборке попадают только "актуальные" (невозвращенные) книги читателя
        if len(reader.borrowed_books) >= settings.reader.READERS_MAX_ITEMS_AT_ONCE:
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": Errors.HANDLER_MESSAGE(),
                    "detail": Errors.LIMIT_REACHED()
                }
            )

        #  Вернет ответ с ошибкой ORJSONResponse, если у читателя уже есть такая книга "на руках"
        # В borrowed_books по выборке попадают только "актуальные" (невозвращенные) книги читателя
        reader_books = [book.book_id for book in reader.borrowed_books]
        if book.id in reader_books:
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": Errors.HANDLER_MESSAGE(),
                    "detail": Errors.SIMILAR_EXISTS()
                }
            )

        instance: BorrowedBookCreate = BorrowedBookCreate(
            book_id=book.id,
            reader_id=reader.id,
        )

        book_instance: BookUpdatePartial = BookUpdatePartial(
            quantity=book.quantity - 1
        )

        repository: LibraryRepository = LibraryRepository(
            session=self.session
        )
        try:
            result = await repository.create_one(
                instance=instance
            )
        except CustomException as exc:
            return ORJSONResponse(
                status_code=exc.status_code,
                content={
                    "message": Errors.HANDLER_MESSAGE(),
                    "detail": exc.msg,
                }
            )

        #  В случае успешного создания экземпляра "выдачи" BorrowedBook уменьшаем количество
        # экземпляров текущей книги на складе на 1
        if result:
            book_service: BookService = BookService(
                session=self.session
            )
            edition_result = await book_service.edit_one(
                orm_model=book,
                instance=book_instance,
                is_partial=True,
            )
            if isinstance(edition_result, ORJSONResponse):
                return edition_result
        return result

    async def return_one(
            self,
            orm_model: "BorrowedBook"
    ):
        #  Вернет ответ с ошибкой ORJSONResponse, если нет записей в бд по выбранному  borrowed_id
        if isinstance(orm_model, ORJSONResponse):
            return orm_model

        #  Вернет ответ с ошибкой ORJSONResponse, если книга уже возвращена
        if orm_model.return_date is not None:
            return ORJSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "message": Errors.HANDLER_MESSAGE(),
                    "detail": Errors.INVALID_OPERATION(),
                }
            )

        #  Фиксируем в бд дату и время возврата книги
        repository: LibraryRepository = LibraryRepository(
            session=self.session
        )
        orm_model.return_date = datetime.now()
        try:
            result = await repository.save(orm_model)
        except CustomException as exc:
            return ORJSONResponse(
                status_code=exc.status_code,
                content={
                    "message": Errors.HANDLER_MESSAGE(),
                    "detail": exc.msg,
                }
            )

        # В случае успешного добавления времени возрата книги в бд увеличиваем количество экземпляров
        # возвращенной книги на 1
        if result:
            book_service: BookService = BookService(
                session=self.session
            )
            try:
                book = await book_service.get_one(
                    id=result.book_id
                )
            except CustomException as exc:
                return ORJSONResponse(
                    status_code=exc.status_code,
                    content={
                        "message": Errors.HANDLER_MESSAGE(),
                        "detail": exc.msg,
                    }
                )
            book_instance: BookUpdatePartial = BookUpdatePartial(
                quantity=book.quantity + 1
            )
            edition_result = await book_service.edit_one(
                orm_model=book,
                instance=book_instance,
                is_partial=True,
            )
            if isinstance(edition_result, ORJSONResponse):
                return edition_result
        return result

    async def get_actual_info(
            self,
            reader: "Reader"
    ):
        #  Вернет ответ с ошибкой ORJSONResponse, если нет читателя в бд по выбранному  id
        if isinstance(reader, ORJSONResponse):
            return reader

        return sorted([b_book.book for b_book in reader.borrowed_books], key=lambda x: x.id)

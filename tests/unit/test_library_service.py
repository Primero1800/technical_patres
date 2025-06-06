import json
from datetime import datetime, timedelta
from unittest.mock import MagicMock, AsyncMock, patch

import pytest

from fastapi.responses import ORJSONResponse

from src.api.v1.library.service import LibraryService
from src.api.v1.library.exceptions import Errors
from src.core.models import BorrowedBook

from .fixtures import *


@pytest.mark.asyncio
async def test_borrow_one_below_limit(
        mock_session,
        mock_book_q5,
        mock_reader,
):
    """Проверка, если читатель не достиг лимита и книга есть в наличии"""

    # Мокирование репозитория для возврата обновленного экземпляра
    mock_repo = MagicMock()
    mock_repo.create_one = AsyncMock(
        return_value=BorrowedBook(
            book_id=mock_book_q5.id,
            reader_id=mock_reader.id,
            borrow_date=datetime.now(),
            return_date=None,
        )
    )

    with patch('src.api.v1.library.service.LibraryRepository', return_value=mock_repo):
        service: LibraryService = LibraryService(
            session=mock_session
        )
        response = await service.borrow_one(
            book=mock_book_q5,
            reader=mock_reader
        )

    assert isinstance(response, BorrowedBook)
    assert response.book_id == mock_book_q5.id
    assert response.reader_id == mock_reader.id
    assert response.return_date is None
    assert isinstance(response.borrow_date, datetime)
    assert response.borrow_date < datetime.now()


@pytest.mark.asyncio
async def test_borrow_one_limit_reached(
        mock_session,
        mock_book_q5,
        mock_reader_limit,
):
    """Проверка, если читатель достиг лимита, но книга есть в наличии"""
    service: LibraryService = LibraryService(
        session=mock_session
    )
    response = await service.borrow_one(
        book=mock_book_q5,
        reader=mock_reader_limit
    )

    assert isinstance(response, ORJSONResponse)
    assert response.status_code == 400
    assert json.loads(response.body.decode()) == {
        "message": Errors.HANDLER_MESSAGE(),
        "detail": Errors.LIMIT_REACHED()
    }


@pytest.mark.asyncio
async def test_borrow_not_enough_quantity(
        mock_session,
        mock_reader,
        mock_book_q0
):
    """Проверка, если книги нет в наличии (количество книг на руках читателя не важно)"""
    service: LibraryService = LibraryService(
        session=mock_session
    )
    response = await service.borrow_one(
        book=mock_book_q0,
        reader=mock_reader
    )

    assert isinstance(response, ORJSONResponse)
    assert response.status_code == 400
    assert json.loads(response.body.decode()) == {
        "message": Errors.HANDLER_MESSAGE(),
        "detail": Errors.NOT_ENOUGH_QUANTITY()
    }


@pytest.mark.asyncio
async def test_borrow_one_with_book_on_hands(
        mock_session,
        mock_book_q5,
        mock_reader_with_1,
):
    """Проверка, если читатель не достиг лимита, книга есть в наличии,
    но такая кинга у него уже есть на руках"""
    service: LibraryService = LibraryService(
        session=mock_session
    )
    response = await service.borrow_one(
        book=mock_book_q5,
        reader=mock_reader_with_1
    )

    assert isinstance(response, ORJSONResponse)
    assert response.status_code == 400
    assert json.loads(response.body.decode()) == {
        "message": Errors.HANDLER_MESSAGE(),
        "detail": Errors.SIMILAR_EXISTS()
    }


@pytest.mark.asyncio
async def test_borrow_one_without_book_on_hands(
        mock_session,
        mock_book_q5,
        mock_reader_without_1
):
    """Проверка, если читатель не достиг лимита, книга есть в наличии,
    и такая книга у него уже ранее была на руках"""

    # Мокирование репозитория для возврата обновленного экземпляра
    mock_repo = MagicMock()
    mock_repo.create_one = AsyncMock(
        return_value=BorrowedBook(
            book_id=mock_book_q5.id,
            reader_id=mock_reader_without_1.id,
            borrow_date=datetime.now(),
            return_date=None,
        )
    )

    with patch('src.api.v1.library.service.LibraryRepository', return_value=mock_repo):
        service: LibraryService = LibraryService(
            session=mock_session
        )
        response = await service.borrow_one(
            book=mock_book_q5,
            reader=mock_reader_without_1
        )

    assert isinstance(response, BorrowedBook)
    assert response.book_id == mock_book_q5.id
    assert response.reader_id == mock_reader_without_1.id
    assert response.return_date is None
    assert isinstance(response.borrow_date, datetime)
    assert response.borrow_date < datetime.now()


@pytest.mark.asyncio
async def test_return_one_already_returned(
        mock_session,
        mock_borrowed_book_returned,
):
    """Проверка попытки возврата уже возвращенной книги"""
    service: LibraryService = LibraryService(
        session=mock_session
    )
    response = await service.return_one(
        orm_model=mock_borrowed_book_returned
    )

    assert isinstance(response, ORJSONResponse)
    assert response.status_code == 400
    assert json.loads(response.body.decode()) == {
        "message": Errors.HANDLER_MESSAGE(),
        "detail": Errors.INVALID_OPERATION()
    }


@pytest.mark.asyncio
async def test_return_one_not_returned(
        mock_session,
        mock_borrowed_book,
):
    """Проверка попытки возврата еще не возвращенной книги"""

    # Мокирование репозитория для возврата обновленного экземпляра
    mock_repo = MagicMock()
    mock_repo.save = AsyncMock(
        return_value=BorrowedBook(
            id=mock_borrowed_book.id,
            book_id=mock_borrowed_book.book_id,
            reader_id=mock_borrowed_book.reader_id,
            borrow_date=mock_borrowed_book.borrow_date,
            return_date=datetime.now() - timedelta(seconds=5),
        )
    )

    with patch('src.api.v1.library.service.LibraryRepository', return_value=mock_repo):
        service: LibraryService = LibraryService(
            session=mock_session
        )
        response = await service.return_one(
            orm_model=mock_borrowed_book
        )

    assert isinstance(response, BorrowedBook)
    assert response.book_id == mock_borrowed_book.book_id
    assert isinstance(response.return_date, datetime)
    assert response.return_date < datetime.now()

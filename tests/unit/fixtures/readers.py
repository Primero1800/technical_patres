from datetime import datetime
from unittest.mock import MagicMock

import pytest

from src.core.models import BorrowedBook
from src.core.settings import settings


@pytest.fixture
def mock_reader_limit():
    # Создаем мок-читателя с максимально возможным набранным числом книг
    mock_reader = MagicMock()
    mock_reader.id = 1
    mock_reader.borrowed_books = [
        MagicMock() for _ in range(settings.reader.READERS_MAX_ITEMS_AT_ONCE)
    ]
    return mock_reader


@pytest.fixture
def mock_reader():
    # Создаем мок-читателя с набранным количеством книг меньше максимального
    mock_reader = MagicMock()
    mock_reader.id = 1
    mock_reader.borrowed_books = [
        MagicMock() for _ in range(settings.reader.READERS_MAX_ITEMS_AT_ONCE - 1)
    ]
    return mock_reader


@pytest.fixture
def mock_reader_with_1():
    # Создаем мок-читателя с набранным количеством книг меньше максимального,
    # но имеющего на руках книгу с book_id=1
    mock_reader = MagicMock()
    mock_reader.id = 1
    mock_reader.borrowed_books = [
        BorrowedBook(
            id=1,
            reader_id=1,
            book_id=1,
            borrow_date=datetime.now(),
            return_date=None
        )
    ]
    return mock_reader


@pytest.fixture
def mock_reader_without_1():
    # Создаем мок-читателя с набранным количеством книг меньше максимального,
    # но имевшего ранее на руках книгу с book_id=1
    mock_reader = MagicMock()
    mock_reader.id = 1
    mock_reader.borrowed_books = [
        # Список пустой, потому что выборка из базы данных вернет только
        # актуальные экземпляры книг (которые на руках) и проигнорирует ранее возвращенные
    ]
    return mock_reader

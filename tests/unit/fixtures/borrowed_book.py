from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_borrowed_book():
    # Создаем выдачу книги без возврата
    mock_bbook = MagicMock()
    mock_bbook.id = 1
    mock_bbook.reader_id = 1
    mock_bbook.book_id = 1
    mock_bbook.borrow_date = datetime.now() - timedelta(seconds=5)
    mock_bbook.return_date = None
    return mock_bbook


@pytest.fixture
def mock_borrowed_book_returned(
        mock_borrowed_book,
):
    # Создаем выдачу книги, уже возвращенную
    mock_borrowed_book.return_date = datetime.now()
    return mock_borrowed_book

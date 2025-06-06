from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_book_q5():
    # Создаем мок-книгу с количеством 5 на складе
    book = MagicMock()
    book.id = 1
    book.quantity = 5
    return book


@pytest.fixture
def mock_book_q0():
    # Создаем мок-книгу с количеством 0 на складе
    book = MagicMock()
    book.id = 1
    book.quantity = 0
    return book

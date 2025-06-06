from unittest.mock import MagicMock

import pytest

from src.core.settings import settings


@pytest.fixture
def mock_reader_limit():
    # Создаем мок-читателя с максимально возможным набранным числом книг
    mock_reader = MagicMock()
    mock_reader.borrowed_books = [
        MagicMock() for _ in range(settings.reader.READERS_MAX_ITEMS_AT_ONCE)
    ]
    return mock_reader


@pytest.fixture
def mock_reader():
    # Создаем мок-читателя с набранным количеством книг меньше максимального
    mock_reader = MagicMock()
    mock_reader.borrowed_books = [
        MagicMock() for _ in range(settings.reader.READERS_MAX_ITEMS_AT_ONCE - 1)
    ]
    return mock_reader

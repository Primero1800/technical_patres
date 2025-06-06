import pytest

from unittest.mock import AsyncMock


@pytest.fixture
def mock_session():
    return AsyncMock()

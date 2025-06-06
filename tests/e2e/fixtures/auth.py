import json

import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from src.main import app

TEST_USER = "test_user@test.com"
TEST_PASSWORD = "12345678"


@pytest_asyncio.fixture(loop_scope='session')
async def test_client():
    """
    Создает один AsyncClient для всех тестов в модуле/сессии.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture(loop_scope="session")
async def register_user(test_client):
    """
    Регистрирует нового пользователя через API.
    """
    registration_data = {
        "email": TEST_USER,
        "password": TEST_PASSWORD,
    }
    response = await test_client.post(
        "/api/v1/auth/register",
        json=registration_data
    )
    return response


@pytest_asyncio.fixture(loop_scope="session")
async def token(test_client, register_user):
    """
    Аутентификация созданного пользователя.
    """
    auth_data = {
        "username": TEST_USER,
        "password": TEST_PASSWORD,
    }
    response = await test_client.post(
        "/api/v1/auth/login",
        data=auth_data
    )
    print(response)
    assert response.status_code == 200
    return json.loads(response.content)['access_token']

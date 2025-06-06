import pytest

from .fixtures import *


@pytest.mark.asyncio(loop_scope="session")
async def test_readers_full_without_token(test_client):
    """
    Проверка доступа к защищенному эндпоинту без токена — должно возвращать 401.
    """
    response = await test_client.get("/api/v1/readers/full")
    assert response.status_code == 401


@pytest.mark.asyncio(loop_scope="session")
async def test_readers_full_with_token(test_client, token):
    """
    Проверка доступа к защищенному эндпоинту с валидным токеном.
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = await test_client.get("/api/v1/readers/full", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


@pytest.mark.asyncio(loop_scope="session")
async def test_readers_full_with_invalid_token(test_client, token):
    """
    Проверка с некорректным токеном — должно возвращать 401.
    """

    headers = {
        "Authorization": f"Bearer {token}_invalid"
    }
    response = await test_client.get("/api/v1/readers/full", headers=headers)
    assert response.status_code == 401

from unittest.mock import MagicMock

import pytest
from httpx import AsyncClient
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.testclient import TestClient

from backend.src.main import app


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
async def test_session() -> AsyncSession:
    """
    Прописать подключение взависимости от того, где развернута тестовая бд
    на усройстве или в контейнере
    """


@pytest.fixture
async def mock_redis() -> MagicMock:
    mock = MagicMock(spec=Redis)
    mock.get = MagicMock(return_value=None)
    mock.set = MagicMock(return_value=None)
    return mock


@pytest.mark.asyncio
async def test_registration(client: AsyncClient, test_session: AsyncSession):
    registration_data = {
        "email": "test@example.com",
        "password": "testpassword",
    }
    response = await client.post("/registration", json=registration_data)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_login(client: AsyncClient, test_session: AsyncSession):

    login_data = {
        "email": "test@example.com",
        "password": "testpassword",
    }
    response = await client.post("/login", data=login_data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient, test_session: AsyncSession):
    response = await client.get("/current-user")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_logout(client: AsyncClient):
    response = await client.post("/logout")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_send_email_confirmation(client: AsyncClient, mock_redis: MagicMock):
    send_code_data = {
        "email": "test@example.com"
    }
    response = await client.post("/send-email-confirmation", json=send_code_data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_confirm_email(client: AsyncClient, mock_redis: MagicMock, test_session: AsyncSession):
    code = mock_redis.get("test@example.com")

    confirm_code_data = {
        "email": "test@example.com",
        "code": code
    }
    response = await client.post("/confirm-email", json=confirm_code_data)
    assert response.status_code == 200

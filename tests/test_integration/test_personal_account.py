import pytest
from httpx import AsyncClient
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


@pytest.mark.asyncio
async def test_get_user_orders(client: AsyncClient, test_session: AsyncSession):
    response = await client.get("/get-user-orders?user_id=1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_cart(client: AsyncClient, test_session: AsyncSession):
    response = await client.get("/get-user-cart?user_id=1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_to_cart(client: AsyncClient, test_session: AsyncSession):
    data = {"user_id": 1, "carpet_id": 1}
    response = await client.post("/add-to-cart", json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_remove_from_cart(client: AsyncClient, test_session: AsyncSession):
    data = {"user_id": 1, "carpet_id": 1}
    response = await client.delete("/remove-from-cart", json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_favorite(client: AsyncClient, test_session: AsyncSession):
    response = await client.get("/get-user-favorite?user_id=1")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_to_favorite(client: AsyncClient, test_session: AsyncSession):
    data = {"user_id": 1, "carpet_id": 1}
    response = await client.post("/add-to-favorite", json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_remove_from_favorite(client: AsyncClient, test_session: AsyncSession):
    data = {"user_id": 1, "carpet_id": 1}
    response = await client.delete("/remove-from-favorite", json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, test_session: AsyncSession):
    data = {"user_update": {"email": "new_email"}, "session": test_session}
    response = await client.patch("/update-user-by-id", json=data)
    assert response.status_code == 200

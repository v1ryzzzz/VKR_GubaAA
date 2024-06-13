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
async def test_generate_image(client: AsyncClient):
    response = await client.post("/api/v1/generate-carpet", json={"prompt": "image"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_carpet(client: AsyncClient, test_session: AsyncSession):
    carpet_data = {
        "title": "Test Carpet",
        "description": "A beautiful test carpet",
        "price": 100,
        "discount": 10,
        "img": "test_img",
        "style": "Modern",
        "material": "Wool",
        "size": "test_size",
        "form": "Rectangle",
        "color": "Red",
        "pattern": "Striped"
    }
    response = await client.post("/api/v1/create-carpet", json=carpet_data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_all_carpets(client: AsyncClient):
    response = await client.get("/api/v1/get-all-carpets")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_carpet(client: AsyncClient):
    response = await client.get("/api/v1/get-carpet", params={"carpet_id": 1})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_carpet(client: AsyncClient):
    response = await client.delete("/api/v1/delete-carpet-by-id", params={"carpet_id": 1})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_carpet(client: AsyncClient):
    update_data = {
        "title": "Updated Test Carpet",
        "description": "An updated beautiful test carpet",
        "price": 150,
        "discount": 15,
        "img": "test",
        "style": "Contemporary",
        "material": "Silk",
        "size": "test",
        "form": "Square",
        "color": "Blue",
        "pattern": "Geometric"
    }
    response = await client.patch("/api/v1/update-carpet-by-id", json=update_data)
    assert response.status_code == 200

import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Carpet
from carpets.schemas import GenerateImage, CarpetCreate, CarpetUpdatePartial, CarpetsFilterParams
from backend.src.carpets.service import (
    generate_image_service, create_carpet_service,
    get_all_carpets_service, get_public_carpets_service, get_user_carpets_service,
    get_carpet_by_id_service, get_carpet_by_title_service, delete_carpet_by_id_service,
    update_carpet_service
)


@pytest.mark.asyncio
async def test_generate_image_service():
    image_data = GenerateImage(prompt="test prompt", width=256, height=256)

    with patch('carpets.accessor.Text2ImageAPI.get_model', return_value="model_id"):
        with patch('carpets.accessor.Text2ImageAPI.generate', return_value="request_id"):
            with patch('carpets.accessor.Text2ImageAPI.check_generation', return_value="generated_image"):
                response = await generate_image_service(image_data)

    assert response.status_code == 200
    assert response.json() == {"image": "generated_image"}


@pytest.mark.asyncio
async def test_create_carpet_service():
    create_carpet_credential = CarpetCreate(
        title="Test Carpet",
        description="Test Description",
        price=100,
        discount=10,
        img="test_img",
        style="modern",
        material="wool",
        size="5x7",
        visibility_status="public"
    )
    db_session = AsyncMock(AsyncSession)

    response = await create_carpet_service(create_carpet_credential, db_session)

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_all_carpets_service():
    carpets_filter = CarpetsFilterParams(title="Test Carpet")
    db_session = AsyncMock(AsyncSession)
    carpet = Carpet(id=1, title="Test Carpet", style="modern", material="wool", size="5x7")

    db_session.execute.return_value.scalars.return_value.all.return_value = [carpet]

    response = await get_all_carpets_service(carpets_filter, db_session)

    assert len(response) == 1


@pytest.mark.asyncio
async def test_get_carpet_by_id_service():
    carpet_id = 1
    db_session = AsyncMock(AsyncSession)
    carpet = Carpet(id=carpet_id, title="Test Carpet")

    db_session.execute.return_value.scalar.return_value = carpet

    response = await get_carpet_by_id_service(carpet_id, db_session)

    assert response.id == carpet_id


@pytest.mark.asyncio
async def test_delete_carpet_by_id_service():
    carpet_id = 1
    db_session = AsyncMock(AsyncSession)
    carpet = Carpet(id=carpet_id, title="Test Carpet")

    db_session.execute.return_value.scalar.return_value = carpet

    response = await delete_carpet_by_id_service(carpet_id, db_session)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_carpet_service():
    carpet_update = CarpetUpdatePartial(id=1, title="Updated Carpet")
    db_session = AsyncMock(AsyncSession)
    carpet = Carpet(id=1, title="Test Carpet")

    db_session.execute.return_value.scalar.return_value = carpet

    response = await update_carpet_service(carpet_update, db_session)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_public_carpets_service():
    carpets_filter = CarpetsFilterParams(style="modern")
    db_session = AsyncMock(AsyncSession)
    carpet = Carpet(id=1, title="Test Carpet", style="modern", visibility_status="public")

    db_session.execute.return_value.scalars.return_value.all.return_value = [carpet]

    response = await get_public_carpets_service(carpets_filter, db_session)

    assert len(response) == 1


@pytest.mark.asyncio
async def test_get_user_carpets_service():
    user_id = 1
    db_session = AsyncMock(AsyncSession)
    carpet = Carpet(id=1, title="Test Carpet", visibility_status=str(user_id))

    db_session.execute.return_value.scalars.return_value.all.return_value = [carpet]

    response = await get_user_carpets_service(user_id, db_session)

    assert len(response) == 1


@pytest.mark.asyncio
async def test_get_carpet_by_title_service():
    title = "Test Carpet"
    db_session = AsyncMock(AsyncSession)
    carpet = Carpet(id=1, title=title)

    db_session.execute.return_value.scalar.return_value = carpet

    response = await get_carpet_by_title_service(title, db_session)

    assert response.id == 1

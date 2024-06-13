import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from core.models import Order, Favorite, Cart, User
from users.schemas import UserUpdatePartial

from backend.src.personal_account.service import (
    _get_user_orders, _get_user_favorites, _add_to_favorite,
    _remove_from_favorite, _get_user_cart, _add_to_cart,
    _remove_from_cart, update_user_service, send_recovery_password_service,
    confirm_password_code_service, change_password_service
)


@pytest.mark.asyncio
async def test_get_user_orders():
    user_id = 1
    db_session = AsyncMock(AsyncSession)
    order = Order(id=1, user_id=user_id)

    db_session.execute.return_value.scalars.return_value.all.return_value = [order]

    response = await _get_user_orders(user_id, db_session)

    assert len(response) == 1


@pytest.mark.asyncio
async def test_get_user_favorites():
    user_id = 1
    db_session = AsyncMock(AsyncSession)
    favorite = Favorite(id=1, user_id=user_id)

    db_session.execute.return_value.scalars.return_value.all.return_value = [favorite]

    response = await _get_user_favorites(user_id, db_session)

    assert len(response) == 1


@pytest.mark.asyncio
async def test_add_to_favorite():
    user_id = 1
    carpet_id = 1
    db_session = AsyncMock(AsyncSession)

    response = await _add_to_favorite(user_id, carpet_id, db_session)

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_remove_from_favorite():
    user_id = 1
    carpet_id = 1
    db_session = AsyncMock(AsyncSession)
    favorite = Favorite(id=1, user_id=user_id, carpet_id=carpet_id)

    db_session.execute.return_value.scalar.return_value = favorite

    response = await _remove_from_favorite(user_id, carpet_id, db_session)

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_user_cart():
    user_id = 1
    db_session = AsyncMock(AsyncSession)
    cart = Cart(id=1, user_id=user_id)

    db_session.execute.return_value.scalars.return_value.all.return_value = [cart]

    response = await _get_user_cart(user_id, db_session)

    assert len(response) == 1


@pytest.mark.asyncio
async def test_add_to_cart():
    user_id = 1
    carpet_id = 1
    db_session = AsyncMock(AsyncSession)

    response = await _add_to_cart(user_id, carpet_id, db_session)

    assert response.status_code == 201
    assert response.json() == {"detail": "Carpet add successfully"}


@pytest.mark.asyncio
async def test_remove_from_cart():
    user_id = 1
    carpet_id = 1
    db_session = AsyncMock(AsyncSession)
    cart = Cart(id=1, user_id=user_id, carpet_id=carpet_id)

    db_session.execute.return_value.scalar.return_value = cart

    response = await _remove_from_cart(user_id, carpet_id, db_session)

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_update_user_service():
    user_id = 1
    user_update = UserUpdatePartial(first_name="Updated Name")
    db_session = AsyncMock(AsyncSession)
    user = User(id=user_id, name="Old Name")

    db_session.execute.return_value.scalar.return_value = user

    response = await update_user_service(user_id, user_update, db_session)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_send_recovery_password_service():
    email = "test@example.com"
    redis = AsyncMock(Redis)
    code = "123456"

    with patch('personal_account.utils.generate_password_code', return_value=code):
        with patch('notification.service.send_email_service', return_value=None):
            response = await send_recovery_password_service(email, redis)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_confirm_password_code_service():
    email = "test@example.com"
    code = "123456"
    redis = AsyncMock(Redis)
    redis.get.return_value = code.encode()

    response = await confirm_password_code_service(email, code, redis)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_change_password_service():
    email = "test@example.com"
    new_password = "new_password"
    code = "123456"
    redis = AsyncMock(Redis)
    db_session = AsyncMock(AsyncSession)
    user = User(id=1, email=email, password="old_password")

    redis.get.return_value = code.encode()
    db_session.execute.return_value.scalar.return_value = user

    response = await change_password_service(email, new_password, code, redis, db_session)

    assert response.status_code == 200

import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from starlette.responses import JSONResponse
from auth.schemas import Registration, Login
from backend.src.auth.service import (
    registration_service, login_service,
    _logout, _send_email_confirmation, _confirm_email
)


@pytest.mark.asyncio
async def test_registration_service():
    register_credential = Registration(email="test@example.com", password="password123")
    db_session = AsyncMock(AsyncSession)

    with patch('auth.utils.hash_password', return_value="hashed_password"):
        with patch('users.service.create_user_service', return_value={"id": 1, "email": "test@example.com"}):
            response = await registration_service(register_credential, db_session)

    assert response['email'] == "test@example.com"


@pytest.mark.asyncio
async def test_login_service_success():
    login_credential = Login(email="test@example.com", password="password123")
    db_session = AsyncMock(AsyncSession)

    user = AsyncMock()
    user.email = "test@example.com"
    user.password = "hashed_password"
    user.id = 1
    user.is_admin = False

    with patch('users.service.get_user_by_email_service', return_value=user):
        with patch('auth.utils.validate_password', return_value=True):
            with patch('auth.services._create_token_service', return_value=JSONResponse(status_code=200)):
                response = await login_service(login_credential, db_session)

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_service_invalid_password():
    login_credential = Login(email="test@example.com", password="wrongpassword")
    db_session = AsyncMock(AsyncSession)

    user = AsyncMock()
    user.email = "test@example.com"
    user.password = "hashed_password"

    with patch('users.service.get_user_by_email_service', return_value=user):
        with patch('auth.utils.validate_password', return_value=False):
            response = await login_service(login_credential, db_session)

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_logout():
    response = await _logout()
    assert response.status_code == 200
    assert "access_token" not in response.cookies
    assert "refresh_token" not in response.cookies


@pytest.mark.asyncio
async def test_send_email_confirmation():
    email = "test@example.com"
    redis = AsyncMock(Redis)

    with patch('auth.utils.generate_email_confirmation_code', return_value="123456"):
        with patch('notification.service.send_email_service', return_value=None) as send_email_mock:
            await _send_email_confirmation(email, redis)

    redis.set.assert_called_with(email, "123456")
    send_email_mock.assert_called_once()


@pytest.mark.asyncio
async def test_confirm_email_success():
    email = "test@example.com"
    code = "123456"
    redis = AsyncMock(Redis)
    session = AsyncMock(AsyncSession)

    user = AsyncMock()
    user.email = email

    redis.get.return_value = b"123456"

    with patch('users.service.get_user_by_email_service', return_value=user):
        response = await _confirm_email(email, code, redis, session)

    assert response.status_code == 200
    session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_confirm_email_wrong_code():
    email = "test@example.com"
    code = "wrongcode"
    redis = AsyncMock(Redis)
    session = AsyncMock(AsyncSession)

    redis.get.return_value = b"123456"

    with patch('users.service.get_user_by_email_service', return_value=None):
        with pytest.raises(HTTPException) as exc_info:
            await _confirm_email(email, code, redis, session)

    assert exc_info.value.status_code == 400

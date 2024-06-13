from fastapi import APIRouter, Depends, Request, Cookie
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from fastapi.responses import JSONResponse

from auth.schemas import Registration, Login, SendCode, ConfirmCode
from auth.service import registration_service, _create_token_service, _get_current_user, login_service, _logout, \
    _send_email_confirmation, _confirm_email
from core.models import db_helper
from core.redis.session import get_redis_email_confirmations

router = APIRouter(tags=["Auth"])


@router.post("/registration")
async def registration(
        register_credential: Registration,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    user = await registration_service(register_credential, session)
    response_obj = JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"detail": "User registration successful"}
    )
    return await _create_token_service(response_obj, user.id)


@router.post("/login")
async def login(
        login_credential: Login,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await login_service(login_credential, session)


@router.get("/current-user")
async def get_current_user(
        access_token: str = Cookie(None),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    if access_token is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "User not auth"}
        )
    return await _get_current_user(access_token, session)


@router.post("/logout")
async def logout():
    return await _logout()


@router.post("/send-email-confirmation")
async def send_email_confirmation(
        data: SendCode,
        redis: Redis = Depends(get_redis_email_confirmations)
):
    await _send_email_confirmation(data.email, redis)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "email send successful"}
    )


@router.post("/confirm-email")
async def confirm_email(
        data: ConfirmCode,
        redis: Redis = Depends(get_redis_email_confirmations),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await _confirm_email(data.email, data.code, redis, session)

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import Response, JSONResponse
from fastapi import Request, HTTPException
from auth.schemas import Registration, Login
from auth.utils import hash_password, create_access_token, create_refresh_token, decode_jwt, validate_password, \
    generate_email_confirmation_code
from core.config import COOKIE_TIME_EXPIRE
from notification.schemas import EmailData
from notification.service import send_email_service
from users.schemas import UserCreate
from users.service import create_user_service, get_user_by_id_service, get_user_by_email_service


async def registration_service(
        register_credential: Registration,
        db_session: AsyncSession
):
    hashed_password = hash_password(
        register_credential.password
    )
    email = register_credential.email.lower()
    user_create = UserCreate(
        email=email,
        password=hashed_password,
        is_admin=False,
    )
    return await create_user_service(user_create, db_session)


async def login_service(
        login_credential: Login,
        db_session: AsyncSession
):
    email = login_credential.email.lower()
    user = await get_user_by_email_service(email, db_session)
    if user is None:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Incorrect email or password"}
        )
    if not validate_password(login_credential.password, user.password):
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"detail": "Incorrect email or password"}
        )
    response_obj = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "detail": "User login successful",
            "id": user.id,
            "email": user.email,
            "is_admin": user.is_admin
        }
    )
    return await _create_token_service(response_obj, user.id)


async def _get_current_user(
        access_token: str,
        db_session: AsyncSession
):
    token = decode_jwt(access_token)
    user_id = token['sub']
    user = await get_user_by_id_service(user_id, db_session)
    return user


async def _create_token_service(
        response_obj: Response,
        user_id: int
):
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    response_obj.set_cookie(
        key="access_token",
        value=access_token,
        expires=COOKIE_TIME_EXPIRE,
        secure=False,
        httponly=False,
    )
    response_obj.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=COOKIE_TIME_EXPIRE,
        secure=False,
        httponly=False,
    )
    return response_obj


async def _logout():
    response_obj = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"detail": "User logout successful"}
    )
    response_obj.delete_cookie(
        key="access_token",
        secure=False,
        httponly=False,
    )
    response_obj.delete_cookie(
        key="refresh_token",
        secure=False,
        httponly=False,
    )
    return response_obj


async def _send_email_confirmation(
        email: str,
        redis: Redis
):
    code = generate_email_confirmation_code()
    await redis.set(email, code)
    email_data = {
        "receiver_email": email,
        "subject": "Код подтверждения",
        "message": f"Ваш код: {code}"
    }
    email_instance = EmailData(**email_data)
    await send_email_service(email_instance)


async def _confirm_email(
        email: str,
        code: str,
        redis: Redis,
        session: AsyncSession
):
    store_code_byte = await redis.get(email)
    if store_code_byte is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code not found"
        )
    store_code_str = store_code_byte.decode('utf-8')
    if store_code_str == code:
        user = await get_user_by_email_service(email, session)
        if user:
            setattr(user, "email_confirmed", True)
            await session.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        await redis.delete(email)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"detail": "Email confirm successful"}
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Incorrect code"
    )

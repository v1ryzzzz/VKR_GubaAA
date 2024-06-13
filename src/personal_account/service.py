from redis.asyncio import Redis
from sqlalchemy import select
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
from personal_account.utils import generate_password_code
from users.schemas import UserCreate, UserUpdatePartial
from users.service import create_user_service, get_user_by_id_service, get_user_by_email_service

from core.models.user import User
from core.models.order import Order
from core.models.favorite import Favorite
from core.models.cart import Cart


async def _get_user_orders(
        user_id: int,
        session: AsyncSession
):
    stmt = (
        select(Order)
        .where(Order.user_id == user_id)
    )
    result = await session.execute(stmt)
    orders = result.scalars().all()
    return list(orders)


async def _get_user_favorites(
        user_id: int,
        session: AsyncSession
):
    stmt = (
        select(Favorite)
        .where(Favorite.user_id == user_id)
    )
    result = await session.execute(stmt)
    favorites = result.scalars().all()
    return list(favorites)


async def _add_to_favorite(
        user_id: int,
        carpet_id: int,
        session: AsyncSession
):
    favorite = Favorite(
        user_id=user_id,
        carpet_id=carpet_id,
    )
    session.add(favorite)
    await session.commit()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"detail": "Favorite create successfully"}
    )


async def _remove_from_favorite(
        user_id: int,
        carpet_id: int,
        session: AsyncSession
):
    stmt = (
        select(Favorite)
        .where(Favorite.user_id == user_id)
        .where(Favorite.carpet_id == carpet_id)
    )
    result = await session.execute(stmt)
    carpet_in_favorite = result.scalar()
    if carpet_in_favorite is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carpet not found"
        )
    await session.delete(carpet_in_favorite)
    await session.commit()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"detail": "Carpet delete successfully"}
    )


async def _get_user_cart(
        user_id: int,
        session: AsyncSession
):
    stmt = (
        select(Cart)
        .where(Cart.user_id == user_id)
    )
    result = await session.execute(stmt)
    carts = result.scalars().all()
    return list(carts)


async def _add_to_cart(
        user_id: int,
        carpet_id: int,
        session: AsyncSession
):
    cart = Cart(
        user_id=user_id,
        carpet_id=carpet_id,
    )
    session.add(cart)
    await session.commit()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"detail": "Carpet add successfully"}
    )


async def _remove_from_cart(
        user_id: int,
        carpet_id: int,
        session: AsyncSession
):
    stmt = (
        select(Cart)
        .where(Cart.user_id == user_id)
        .where(Cart.carpet_id == carpet_id)
    )
    result = await session.execute(stmt)
    carpet_in_cart = result.scalar()
    if carpet_in_cart is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Carpet not found"
        )
    await session.delete(carpet_in_cart)
    await session.commit()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"detail": "Carpet delete successfully"}
    )


async def update_user_service(
        user_id: int,
        user_update: UserUpdatePartial,
        db_session: AsyncSession
):
    user = await get_user_by_id_service(user_id, db_session)
    if user:
        for name, value in user_update.model_dump().items():
            if value is not None:
                setattr(user, name, value)
        await db_session.commit()
        return JSONResponse(
            content={"detail": "User update successfully"},
            status_code=status.HTTP_200_OK
        )
    raise HTTPException(
        detail="User not found",
        status_code=status.HTTP_404_NOT_FOUND
    )


async def send_recovery_password_service(email: str, redis: Redis):
    code = generate_password_code()
    await redis.set(email, code)
    email_data = {
        "receiver_email": email,
        "subject": "Код подтверждения",
        "message": f"Ваш код: {code}"
    }
    email_instance = EmailData(**email_data)
    await send_email_service(email_instance)
    return JSONResponse(
        content={"detail": "Code send successfully"},
        status_code=status.HTTP_200_OK
    )


async def confirm_password_code_service(
        email: str,
        code: str,
        redis: Redis
):
    store_code_byte = await redis.get(email)
    if store_code_byte is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code not found"
        )
    store_code_str = store_code_byte.decode('utf-8')
    if store_code_str == code:
        return JSONResponse(
            content={
                "detail": "Code correct",
                "code": code
            },
            status_code=status.HTTP_200_OK
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code incorrect"
        )


async def change_password_service(
        email: str,
        new_password: str,
        code: str,
        redis: Redis,
        session: AsyncSession
):
    user = await get_user_by_email_service(email, session)
    if not user:
        raise HTTPException(
            detail="User not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
    store_code_byte = await redis.get(email)
    if store_code_byte is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code not found"
        )
    store_code_str = store_code_byte.decode('utf-8')
    if store_code_str == code:
        await redis.delete(email)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Code incorrect"
        )
    hashed_password = hash_password(new_password)
    setattr(user, "password", hashed_password)
    await session.commit()
    return JSONResponse(
        content={"detail": "Password change successfully"},
        status_code=status.HTTP_200_OK
    )

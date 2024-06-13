from fastapi import APIRouter, Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import current_user
from core.models import db_helper
from core.redis.session import get_redis_password_recovery
from personal_account.schemas import CartCreate, CartRemove, FavoriteCreate, FavoriteRemove, \
    ChangePassword, RecoveryPasswordCode, SendRecoveryPassword
from personal_account.service import _get_user_orders, _get_user_favorites, _get_user_cart, _add_to_cart, \
    _remove_from_cart, _remove_from_favorite, _add_to_favorite, update_user_service, send_recovery_password_service, \
    change_password_service, confirm_password_code_service
from users.schemas import UserUpdatePartial

router = APIRouter(tags=["Personal account"])


@router.get(
    "/get-user-orders",
)
async def get_user_orders(
        user_id: int = Depends(current_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await _get_user_orders(user_id, session)


@router.get(
    "/get-user-cart"
)
async def get_user_cart(
        user_id: int = Depends(current_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await _get_user_cart(user_id, session)


@router.post(
    "/add-to-cart"
)
async def add_to_cart(
        data: CartCreate,
        user_id: int = Depends(current_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await _add_to_cart(user_id, data.carpet_id, session)


@router.delete(
    "/remove-from-cart"
)
async def remove_from_cart(
        data: CartRemove,
        user_id: int = Depends(current_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await _remove_from_cart(user_id, data.carpet_id, session)


@router.get(
    "/get-user-favorite"
)
async def get_user_favorite(
        user_id: int = Depends(current_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await _get_user_favorites(user_id, session)


@router.post(
    "/add-to-favorite"
)
async def add_to_favorite(
        data: FavoriteCreate,
        user_id: int = Depends(current_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await _add_to_favorite(user_id, data.carpet_id, session)


@router.delete(
    "/remove-from-favorite"
)
async def remove_from_favorite(
        data: FavoriteRemove,
        user_id: int = Depends(current_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await _remove_from_favorite(user_id, data.carpet_id, session)


@router.patch("/update-user-by-id")
async def update_user(
        user_update: UserUpdatePartial,
        user_id: int = Depends(current_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await update_user_service(user_id, user_update, session)


@router.post(
    "/send-recovery-password"
)
async def send_recovery_password(
        data: SendRecoveryPassword,
        redis: Redis = Depends(get_redis_password_recovery)
):
    return await send_recovery_password_service(data.email, redis)


@router.post(
    "/check-recovery-password-code"
)
async def send_recovery_password(
        data: RecoveryPasswordCode,
        redis: Redis = Depends(get_redis_password_recovery)
):
    return await confirm_password_code_service(data.email, data.code, redis)


@router.post(
    "/change-password"
)
async def change_password(
        data: ChangePassword,
        redis: Redis = Depends(get_redis_password_recovery),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await change_password_service(
        data.email,
        data.new_password,
        data.code,
        redis,
        session
    )

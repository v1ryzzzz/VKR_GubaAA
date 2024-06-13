from fastapi import APIRouter, Depends, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import is_admin
from core.models import db_helper
from users.service import (
    get_all_users_service,
    get_user_by_id_service,
    delete_user_by_id_service,
    create_user_service,
)
from users.schemas import User, UserCreate

router = APIRouter(tags=["Admin"])


@router.get(
    "/get-all-users",
    response_model=list[User],
    dependencies=[Depends(is_admin)]
)
async def get_users(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await get_all_users_service(db_session=session)


@router.get(
    "/get-user",
    response_model=User,
    dependencies=[Depends(is_admin)]
)
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await get_user_by_id_service(user_id=user_id, db_session=session)


@router.delete(
    "/delete-user-by-id",
    dependencies=[Depends(is_admin)],
)
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await delete_user_by_id_service(user_id=user_id, db_session=session)

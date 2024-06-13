import datetime

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from core.models.user import User
from starlette import status

from .schemas import UserCreate, UserUpdatePartial


async def create_user_service(
        user_credential: UserCreate,
        db_session: AsyncSession
):
    user = User(
        email=user_credential.email,
        password=user_credential.password,
        phone=None,
        is_admin=user_credential.is_admin,
        create_at=datetime.datetime.now()
    )
    db_session.add(user)
    await db_session.commit()
    return user


async def get_all_users_service(db_session: AsyncSession):
    stmt = select(User)
    result = await db_session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user_by_email_service(email: str, db_session: AsyncSession):
    stmt = select(User).where(User.email == email)
    result = await db_session.execute(stmt)
    user = result.scalar()
    return user


async def get_user_by_id_service(user_id: int, db_session: AsyncSession):
    stmt = select(User).where(User.id == user_id)
    result = await db_session.execute(stmt)
    user = result.scalar()
    return user


async def delete_user_by_id_service(
        user_id: int,
        db_session: AsyncSession,
):
    user = await get_user_by_id_service(user_id, db_session)
    if user:
        await db_session.delete(user)
        await db_session.commit()
        return JSONResponse(
            content={"detail": f"User delete successfully"},
            status_code=status.HTTP_200_OK
        )
    raise HTTPException(
        detail=f"User with id: {user_id}, not found",
        status_code=status.HTTP_404_NOT_FOUND
    )

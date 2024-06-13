from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, Depends, Cookie, status

from auth.service import _get_current_user
from core.models import db_helper, User


async def is_admin(
        access_token: str = Cookie(None),
        db: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT token is missing"
        )

    current_user = await _get_current_user(access_token, db)

    if current_user is None or not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return current_user


async def current_user(
    access_token: str = Cookie(None),
    db: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    if access_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT token is missing"
        )

    current_user = await _get_current_user(access_token, db)

    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    return current_user.id

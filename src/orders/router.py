from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from auth.dependencies import is_admin, current_user
from core.models import db_helper
from .service import (
    create_order_service,
    get_all_orders_service, get_order_by_id_service, update_order_status_service, get_user_orders_service
)
from .schemas import Order, OrderCreate, UpdateOrder

router = APIRouter(tags=["Orders"])


@router.post("/create-order")
async def create_carpet(
        create_order_credential: OrderCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await create_order_service(create_order_credential, session)


@router.get(
    "/get-all-orders",
    dependencies=[Depends(is_admin)]
)
async def get_carpets(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await get_all_orders_service(db_session=session)


@router.get(
    "/get-user-orders",
)
async def get_carpets(
        user_id: int = Depends(current_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await get_user_orders_service(user_id=user_id, db_session=session)


@router.get(
    "/get-order-by-id",
    response_model=Order,
    dependencies=[Depends(is_admin)]
)
async def get_order_by_id(
        order_id: int,
        db_session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    order = await get_order_by_id_service(order_id, db_session)
    if order:
        return order
    raise HTTPException(
        detail="Order not found",
        status_code=status.HTTP_404_NOT_FOUND
    )


@router.post(
    "/update-order-by-id",
    dependencies=[Depends(is_admin)]
)
async def update_order_status(
        update_order_credential: UpdateOrder,
        db_session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await update_order_status_service(update_order_credential, db_session)

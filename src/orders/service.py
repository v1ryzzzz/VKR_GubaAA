from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.models import Order
from orders.schemas import OrderCreate, UpdateOrder
from fastapi.responses import JSONResponse
from sqlalchemy import select
from starlette import status

from orders.utils import fake_payment_id


async def create_order_service(
        create_order_credential: OrderCreate,
        db_session: AsyncSession
):
    order = Order(
        user_id=create_order_credential.user_id,
        carpet_id=create_order_credential.carpet_id,
        status="pending",
        payment_id=str(fake_payment_id()),
    )
    db_session.add(order)
    await db_session.commit()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"detail": "Order create successfully"}
    )


async def get_all_orders_service(db_session: AsyncSession):
    stmt = (
        select(Order)
        .options(joinedload(Order.carpet))
    )
    result = await db_session.execute(stmt)
    orders = result.scalars().all()
    return list(orders)


async def get_user_orders_service(user_id: int, db_session: AsyncSession):
    stmt = (
        select(Order)
        .where(Order.user_id == user_id)
        .options(joinedload(Order.carpet))
    )
    result = await db_session.execute(stmt)
    orders = result.scalars().all()
    return list(orders)


async def get_order_by_id_service(
        order_id: int,
        db_session: AsyncSession
):
    stmt = (
        select(Order)
        .where(Order.id == order_id)
    )
    result = await db_session.execute(stmt)
    order = result.scalar()
    return order


async def update_order_status_service(
        update_order_credential: UpdateOrder,
        db_session: AsyncSession
):
    order = await get_order_by_id_service(update_order_credential.order_id, db_session)
    if order:
        setattr(order, "status", update_order_credential.status)
        await db_session.commit()
        return JSONResponse(
            content={"detail": "Order update successfully"},
            status_code=status.HTTP_200_OK
        )
    raise HTTPException(
        detail="Order not found",
        status_code=status.HTTP_404_NOT_FOUNDs
    )

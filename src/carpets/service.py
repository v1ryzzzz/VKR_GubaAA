from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Carpet
from carpets.accessor import Text2ImageAPI
from carpets.schemas import GenerateImage, CarpetCreate, CarpetUpdatePartial, CarpetsFilterParams
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select, and_
from starlette import status


async def generate_image_service(
        image_data: GenerateImage
):
    try:
        model_id = await Text2ImageAPI.get_model()
        request_id = await Text2ImageAPI.generate(
            prompt=image_data.prompt,
            model=model_id,
            width=image_data.width,
            height=image_data.height
        )
        image = await Text2ImageAPI.check_generation(request_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"image": image}
        )
    except BaseException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bad request to ai! Retry!"
        )


async def create_carpet_service(
        create_carpet_credential: CarpetCreate,
        db_session: AsyncSession
):
    carpet = Carpet(
        title=create_carpet_credential.title,
        description=create_carpet_credential.description,
        price=create_carpet_credential.price,
        discount=create_carpet_credential.discount,
        img=create_carpet_credential.img,
        style=create_carpet_credential.style,
        material=create_carpet_credential.material,
        size=create_carpet_credential.size,
        visibility_status=create_carpet_credential.visibility_status
    )
    db_session.add(carpet)
    await db_session.commit()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "detail": "Carpet create successfully",
            "id": carpet.id
        }
    )


async def create_personal_carpet_service(
        create_carpet_credential: CarpetCreate,
        user_id: int,
        db_session: AsyncSession
):
    carpet = Carpet(
        title=create_carpet_credential.title,
        description=create_carpet_credential.description,
        price=create_carpet_credential.price,
        discount=create_carpet_credential.discount,
        img=create_carpet_credential.img,
        style=create_carpet_credential.style,
        material=create_carpet_credential.material,
        size=create_carpet_credential.size,
        visibility_status=str(user_id)
    )
    db_session.add(carpet)
    await db_session.commit()
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "detail": "Carpet create successfully",
            "id": carpet.id
        }
    )


async def get_all_carpets_service(
        carpets_filter: Optional[CarpetsFilterParams],
        db_session: AsyncSession
):
    condition = and_()

    if carpets_filter.title:
        condition = and_(
            condition, Carpet.title.like(carpets_filter.title)
        )
    if carpets_filter.style:
        condition = and_(
            condition, Carpet.style.like(carpets_filter.style)
        )
    if carpets_filter.material:
        condition = and_(
            condition, Carpet.material.like(carpets_filter.material)
        )
    if carpets_filter.size:
        condition = and_(
            condition, Carpet.size.like(carpets_filter.size)
        )
    if carpets_filter.form:
        condition = and_(
            condition, Carpet.form.like(carpets_filter.form)
        )
    if carpets_filter.color:
        condition = and_(
            condition, Carpet.color.like(carpets_filter.color)
        )
    if carpets_filter.pattern:
        condition = and_(
            condition, Carpet.pattern.like(carpets_filter.pattern)
        )

    stmt = (
        select(Carpet)
        .where(condition)
    )
    result = await db_session.execute(stmt)
    carpets = result.scalars().all()
    return list(carpets)


async def get_public_carpets_service(
        carpets_filter: Optional[CarpetsFilterParams],
        db_session: AsyncSession
):
    condition = and_()

    if carpets_filter.title:
        condition = and_(
            condition, Carpet.title.like(carpets_filter.title)
        )
    if carpets_filter.style:
        condition = and_(
            condition, Carpet.style.like(carpets_filter.style)
        )
    if carpets_filter.material:
        condition = and_(
            condition, Carpet.material.like(carpets_filter.material)
        )
    if carpets_filter.size:
        condition = and_(
            condition, Carpet.size.like(carpets_filter.size)
        )
    if carpets_filter.form:
        condition = and_(
            condition, Carpet.form.like(carpets_filter.form)
        )
    if carpets_filter.color:
        condition = and_(
            condition, Carpet.color.like(carpets_filter.color)
        )
    if carpets_filter.pattern:
        condition = and_(
            condition, Carpet.pattern.like(carpets_filter.pattern)
        )

    stmt = (
        select(Carpet)
        .where(condition)
        .where(Carpet.visibility_status.like("public"))
    )
    result = await db_session.execute(stmt)
    carpets = result.scalars().all()
    return list(carpets)


async def get_user_carpets_service(
        user_id: int,
        db_session: AsyncSession
):
    stmt = (
        select(Carpet)
        .where(Carpet.visibility_status.like(str(user_id)))
    )
    result = await db_session.execute(stmt)
    carpets = result.scalars().all()
    return carpets


async def get_carpet_by_id_service(carpet_id: int, db_session: AsyncSession):
    stmt = select(Carpet).where(Carpet.id == carpet_id)
    result = await db_session.execute(stmt)
    carpet = result.scalar()
    return carpet


async def get_carpet_by_title_service(title: str, db_session: AsyncSession):
    stmt = select(Carpet).where(Carpet.title == title)
    result = await db_session.execute(stmt)
    carpet = result.scalar()
    return carpet


async def delete_carpet_by_id_service(
        carpet_id: int,
        db_session: AsyncSession,
):
    carpet = await get_carpet_by_id_service(carpet_id, db_session)
    if carpet:
        await db_session.delete(carpet)
        await db_session.commit()
        return JSONResponse(
            content={"detail": f"Carpet delete successfully"},
            status_code=status.HTTP_200_OK
        )
    raise HTTPException(
        detail=f"Carpet with id: {carpet_id}, not found",
        status_code=status.HTTP_404_NOT_FOUND
    )


async def update_carpet_service(
        carpet_update: CarpetUpdatePartial,
        db_session: AsyncSession
):
    carpet = await get_carpet_by_id_service(carpet_update.id, db_session)
    if carpet:
        for name, value in carpet_update.model_dump().items():
            setattr(carpet, name, value)
        await db_session.commit()
        return JSONResponse(
            content={"detail": "Carpet update successfully"},
            status_code=status.HTTP_200_OK
        )
    raise HTTPException(
        detail="Carpet not found",
        status_code=status.HTTP_404_NOT_FOUND
    )

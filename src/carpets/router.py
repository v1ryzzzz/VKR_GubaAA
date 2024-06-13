from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import is_admin, current_user
from core.models import db_helper
from .service import (
    generate_image_service,
    create_carpet_service,
    get_carpet_by_id_service,
    delete_carpet_by_id_service,
    get_all_carpets_service,
    update_carpet_service, get_public_carpets_service, create_personal_carpet_service, get_user_carpets_service
)
from .schemas import GenerateImage, CarpetCreate, CarpetUpdatePartial, Carpet, CarpetsFilterParams, carpet_query_params

router = APIRouter(tags=["Carpets"])


@router.post("/generate-carpet")
async def generate_image(
        carpet_credential: GenerateImage,
):
    return await generate_image_service(carpet_credential)


@router.post(
    "/create-carpet",
    dependencies=[Depends(is_admin)]
)
async def create_carpet(
        create_carpet_credential: CarpetCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await create_carpet_service(create_carpet_credential, session)


@router.post(
    "/create-personal-carpet",
)
async def create_carpet(
        create_carpet_credential: CarpetCreate,
        user_id: int = Depends(current_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await create_personal_carpet_service(create_carpet_credential, user_id, session)


@router.get("/get-all-carpets", response_model=list[Carpet])
async def get_carpets(
        carpets_filter: Optional[CarpetsFilterParams] = Depends(carpet_query_params),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await get_all_carpets_service(carpets_filter=carpets_filter, db_session=session)


@router.get(
    "/get-public-carpets",
    response_model=list[Carpet]
)
async def get_public_carpets(
        carpets_filter: Optional[CarpetsFilterParams] = Depends(carpet_query_params),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await get_public_carpets_service(carpets_filter=carpets_filter, db_session=session)


@router.get(
    "/get-user-carpets",
    response_model=list[Carpet]
)
async def get_user_carpets(
        user_id: int = Depends(current_user),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await get_user_carpets_service(user_id, session)


@router.get("/get-carpet", response_model=Carpet)
async def get_carpet(
        carpet_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await get_carpet_by_id_service(carpet_id=carpet_id, db_session=session)


@router.delete("/delete-carpet-by-id")
async def delete_carpet(
        carpet_id: int,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await delete_carpet_by_id_service(carpet_id=carpet_id, db_session=session)


@router.patch("/update-carpet-by-id")
async def update_user(
        carpet_update: CarpetUpdatePartial,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await update_carpet_service(carpet_update, session)

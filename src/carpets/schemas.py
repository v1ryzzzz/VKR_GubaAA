from typing import Optional

from pydantic import BaseModel


class GenerateImage(BaseModel):
    prompt: str
    width: int = 1024
    height: int = 1024


class Carpet(BaseModel):
    id: int
    title: str
    description: str | None = None
    price: int | None = None
    discount: int | None = None
    img: str | None = None
    style: str | None = None
    material: str | None = None
    size: str | None = None
    form: str | None = None
    color: str | None = None
    pattern: str | None = None


class CarpetCreate(BaseModel):
    title: str
    description: str | None = None
    price: int | None = None
    discount: int | None = None
    img: str | None = None
    style: str | None = None
    material: str | None = None
    size: str | None = None
    form: str | None = None
    color: str | None = None
    pattern: str | None = None
    visibility_status: str | None = "public"


class CarpetUpdatePartial(BaseModel):
    title: str
    description: str | None = None
    price: int | None = None
    discount: int | None = None
    img: str | None = None
    style: str | None = None
    material: str | None = None
    size: str | None = None
    form: str | None = None
    color: str | None = None
    pattern: str | None = None


class CarpetsFilterParams(BaseModel):
    title: str | None = None
    style: str | None = None
    material: str | None = None
    size: str | None = None
    form: str | None = None
    color: str | None = None
    pattern: str | None = None


async def carpet_query_params(
        title: Optional[str] = None,
        style: Optional[str] = None,
        material: Optional[str] = None,
        size: Optional[str] = None,
        form: Optional[str] = None,
        color: Optional[str] = None,
        pattern: Optional[str] = None,
):
    return CarpetsFilterParams(
        title=title,
        style=style,
        material=material,
        size=size,
        form=form,
        color=color,
        pattern=pattern
    )

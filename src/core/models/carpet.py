import sqlalchemy
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, DateTime
from datetime import datetime
from typing import TYPE_CHECKING

from .base import Base

if TYPE_CHECKING:
    from .order import Order


class Carpet(Base):
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    price: Mapped[int | None] = mapped_column(sqlalchemy.Integer(), nullable=False)
    discount: Mapped[int | None]
    img: Mapped[str | None] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    style: Mapped[str | None]
    material: Mapped[str | None]
    size: Mapped[str | None]
    form: Mapped[str | None]
    color: Mapped[str | None]
    pattern: Mapped[str | None]

    visibility_status: Mapped[str | None] = mapped_column(default=None, nullable=True)

    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    orders: Mapped[list["Order"]] = relationship("Order", back_populates="carpet")

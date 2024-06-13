from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, BigInteger
from datetime import datetime

from .base import Base

if TYPE_CHECKING:
    from .cart import Cart
    from .favorite import Favorite
    from .order import Order


class User(Base):
    email: Mapped[str]
    first_name: Mapped[str] = mapped_column(default="")
    last_name: Mapped[str] = mapped_column(default="")
    patronymic: Mapped[str] = mapped_column(default="")
    address: Mapped[str] = mapped_column(default="")
    password: Mapped[str]
    phone: Mapped[str | None] = mapped_column(unique=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    email_confirmed: Mapped[bool] = mapped_column(default=False, nullable=True)

    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

    carts: Mapped[list["Cart"]] = relationship("Cart", back_populates="user")
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")
    favorites: Mapped[list["Favorite"]] = relationship(
        "Favorite", back_populates="user"
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.email!r})"

    def __repr__(self):
        return str(self)

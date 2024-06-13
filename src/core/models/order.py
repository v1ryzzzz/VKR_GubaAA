from datetime import datetime
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base
from .mixins import UserRelationMixin

if TYPE_CHECKING:
    from .carpet import Carpet


class Order(UserRelationMixin, Base):
    _user_back_populates = "orders"

    status: Mapped[str] = mapped_column(default="consideration")
    payment_id: Mapped[str] = mapped_column(default="test-test-test", nullable=True)
    carpet_id: Mapped[int] = mapped_column(ForeignKey("carpets.id"))
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    carpet: Mapped["Carpet"] = relationship("Carpet", back_populates="orders")



from datetime import datetime
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixin


class Cart(UserRelationMixin, Base):
    _user_back_populates = "carts"

    carpet_id: Mapped[int] = mapped_column(ForeignKey("carpets.id"))
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())

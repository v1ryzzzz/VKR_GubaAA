from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship


class UserRelationMixin:
    _user_id_nullable: bool = False
    _user_back_populates: str | None = None

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("users.id"),
            nullable=cls._user_id_nullable,
        )

    @declared_attr
    def user(cls):
        return relationship(
            "User",
            back_populates=cls._user_back_populates,
        )

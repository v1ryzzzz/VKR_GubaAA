from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    email: str
    phone: str | None = None
    is_admin: bool | None = False


class UserCreate(UserBase):
    password: str | bytes


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserUpdatePartial(BaseModel):
    email: str | None = None
    phone: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None
    address: str | None = None


class UserToken(BaseModel):
    id: int
    email: str

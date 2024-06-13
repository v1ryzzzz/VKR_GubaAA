from pydantic import BaseModel


class CartRemove(BaseModel):
    carpet_id: int


class CartCreate(BaseModel):
    carpet_id: int


class FavoriteRemove(BaseModel):
    carpet_id: int


class FavoriteCreate(BaseModel):
    carpet_id: int


class SendRecoveryPassword(BaseModel):
    email: str


class RecoveryPasswordCode(BaseModel):
    email: str
    code: str


class ChangePassword(BaseModel):
    email: str
    new_password: str
    code: str

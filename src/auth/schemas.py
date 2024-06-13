from pydantic import BaseModel


class Registration(BaseModel):
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class SendCode(BaseModel):
    email: str


class ConfirmCode(BaseModel):
    email: str
    code: str


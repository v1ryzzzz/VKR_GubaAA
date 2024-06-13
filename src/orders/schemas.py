from pydantic import BaseModel


class Order(BaseModel):
    id: int
    user_id: int
    carpet_id: int
    status: str
    payment_id: str | None


class OrderCreate(BaseModel):
    user_id: int
    carpet_id: int


class UpdateOrder(BaseModel):
    order_id: int
    status: str

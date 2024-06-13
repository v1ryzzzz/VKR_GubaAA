from pydantic import BaseModel


class UserPayment(BaseModel):
    order_id: int
    phone: str
    email: str
    price: int

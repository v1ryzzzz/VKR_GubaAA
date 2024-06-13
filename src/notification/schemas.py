from pydantic import BaseModel


class EmailData(BaseModel):
    receiver_email: str
    subject: str
    message: str

from fastapi import APIRouter
from notification.schemas import EmailData
from notification.service import send_email_service

router = APIRouter(tags=["Notification"])


@router.post("/send-email")
async def send_email(
        email_data: EmailData,
):
    await send_email_service(email_data)

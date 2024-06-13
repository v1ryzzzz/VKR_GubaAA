from aiosmtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from core.config import settings
from notification.schemas import EmailData


async def send_email_service(email_data: EmailData):
    smtp = SMTP(
        hostname=settings.smtp_settings.smtp_server,
        port=settings.smtp_settings.smtp_port,
        start_tls=True
    )

    await smtp.connect()
    await smtp.login(settings.smtp_settings.smtp_username, settings.smtp_settings.smtp_password)

    msg = MIMEMultipart()
    msg['From'] = settings.smtp_settings.smtp_username
    msg['To'] = email_data.receiver_email
    msg['Subject'] = email_data.subject

    msg.attach(MIMEText(email_data.message, 'plain', 'utf-8'))
    await smtp.send_message(msg)
    await smtp.quit()

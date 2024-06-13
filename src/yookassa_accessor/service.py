import json
from fastapi.responses import Response
from fastapi.exceptions import HTTPException
from fastapi import status
from yookassa import Configuration
from yookassa.domain.notification import WebhookNotificationEventType, WebhookNotificationFactory
from yookassa import Payment
from yookassa.domain.models.currency import Currency
from yookassa.domain.models.receipt import Receipt, ReceiptItem
from yookassa.domain.common.confirmation_type import ConfirmationType
from yookassa.domain.request.payment_request_builder import PaymentRequestBuilder

from core.config import YOOKASSA_ID, YOOKASSA_SECRET_KEY, YOOKASSA_REDIRECT_URL
from yookassa_accessor.schemas import UserPayment


def my_webhook_handler(request):
    event_json = json.loads(request.body)
    try:
        notification_object = WebhookNotificationFactory().create(event_json)
        response_object = notification_object.object
        if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
        elif notification_object.event == WebhookNotificationEventType.PAYMENT_WAITING_FOR_CAPTURE:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
        elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
        elif notification_object.event == WebhookNotificationEventType.REFUND_SUCCEEDED:
            some_data = {
                'refundId': response_object.id,
                'refundStatus': response_object.status,
                'paymentId': response_object.payment_id,
            }
        elif notification_object.event == WebhookNotificationEventType.DEAL_CLOSED:
            some_data = {
                'dealId': response_object.id,
                'dealStatus': response_object.status,
            }
        elif notification_object.event == WebhookNotificationEventType.PAYOUT_SUCCEEDED:
            some_data = {
                'payoutId': response_object.id,
                'payoutStatus': response_object.status,
                'dealId': response_object.deal.id,
            }
        elif notification_object.event == WebhookNotificationEventType.PAYOUT_CANCELED:
            some_data = {
                'payoutId': response_object.id,
                'payoutStatus': response_object.status,
                'dealId': response_object.deal.id,
            }
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

        Configuration.configure(YOOKASSA_ID, YOOKASSA_SECRET_KEY)
        payment_info = Payment.find_one(some_data['paymentId'])
        if payment_info:
            payment_status = payment_info.status
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    return Response(status_code=status.HTTP_200_OK)


def payment_service(
        user_credential: UserPayment
):
    receipt = Receipt()
    receipt.customer = {"phone": user_credential.phone, "email": user_credential.email}
    receipt.tax_system_code = 1
    receipt.items = [
        ReceiptItem({
            "description": "Product 1",
            "quantity": 1.0,
            "amount": {
                "value": user_credential.price,
                "currency": Currency.RUB
            },
            "vat_code": 2
        })
    ]

    builder = PaymentRequestBuilder()
    builder.set_amount({"value": user_credential.price, "currency": Currency.RUB}) \
        .set_confirmation({"type": ConfirmationType.REDIRECT, "return_url": YOOKASSA_REDIRECT_URL}) \
        .set_capture(False) \
        .set_description(f"Заказ №{user_credential.order_id}") \
        .set_metadata({"orderNumber": user_credential.order_id}) \
        .set_receipt(receipt)

    raw_request = builder.build()
    request = Payment.create(raw_request)
    return request

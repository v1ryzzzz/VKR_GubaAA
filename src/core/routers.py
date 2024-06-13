from fastapi import APIRouter

from core.config import API_PREFIX
from admin.router import router as admin_router
from notification.router import router as notification_router
from carpets.router import router as carpet_router
from orders.router import router as order_router
from auth.router import router as auth_router
from personal_account.router import router as personal_account_router

router = APIRouter(prefix=API_PREFIX)


router.include_router(auth_router, prefix="/auth")
router.include_router(personal_account_router, prefix="/personal-account")
router.include_router(carpet_router, prefix="/carpets")
router.include_router(order_router, prefix="/orders")
router.include_router(notification_router, prefix="/notification")
router.include_router(admin_router, prefix="/admin")

from fastapi import APIRouter

from src.app.api.auth import router as auth_router
from src.app.api.ping import router as ping_router
from src.app.api.record import router as record_router
from src.app.api.user import router as user_router

router = APIRouter()

router.include_router(ping_router)
router.include_router(auth_router, prefix='/token', tags=['Authorization'])
router.include_router(user_router, prefix='/users', tags=['Users'])
router.include_router(record_router, prefix='/records', tags=['Records'])

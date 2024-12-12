from fastapi import APIRouter

from src.app.api.auth import router as auth_router
from src.app.api.ping import router as ping_router

router = APIRouter()

router.include_router(ping_router)
router.include_router(auth_router, prefix='/token', tags=['Authorization'])

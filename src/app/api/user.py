from fastapi import APIRouter, Depends

from src.app.schema.user import GetCurrentUserInfoDetail
from src.utils.user import get_current_user

router = APIRouter()


@router.get(
    '/me',
    summary='Get current user info',
    description='Provide the current user information.',
)
async def get_cur_user(data: GetCurrentUserInfoDetail = Depends(get_current_user)) -> GetCurrentUserInfoDetail:
    return data

from http.client import HTTPException

from authx import TokenPayload
from fastapi import Depends

from src.app.model import User
from src.common.security import security
from src.database import CurrentSession


async def get_current_user(db: CurrentSession, payload: TokenPayload = Depends(security.access_token_required)) -> User:
    """
    Get the current user through token

    :param db:
    :param payload:
    :return:
    """
    from src.app.crud.user import user_dao

    user = await user_dao.get_with_relation(db, username=payload.sub)

    if not user.is_active:
        raise HTTPException(401, 'The user has been locked, please contact the system administrator')

    return user

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from authx import TokenPayload
from fastapi import Depends, HTTPException

from src.app.crud.user import user_dao
from src.app.schema.token import GetLoginToken, GetNewToken
from src.app.schema.user import AuthLoginParam
from src.common.security import security
from src.database import async_db_session
from src.utils.password import password_verify


class AuthService:
    @staticmethod
    async def new_token(*, obj: AuthLoginParam) -> GetLoginToken:
        async with async_db_session.begin() as db:
            current_user = await user_dao.get_by_username(db, obj.username)

        if not current_user:
            raise HTTPException(404, 'Incorrect username or password')

        if not password_verify(obj.password, current_user.hashed_password):
            raise HTTPException(404, 'Incorrect username or password')
        elif not current_user.is_active:
            raise HTTPException(401, 'The user has been locked, please contact the system administrator')

        current_username = current_user.username

        date_now = datetime.now()
        access_token = security.create_access_token(current_username)
        refresh_token = security.create_refresh_token(current_username)

        return GetLoginToken(
            access_token=access_token,
            access_token_expire_time=date_now + security.config.JWT_ACCESS_TOKEN_EXPIRES,
            refresh_token=refresh_token,
            refresh_token_expire_time=date_now + security.config.JWT_REFRESH_TOKEN_EXPIRES,
            user=current_user,  # type: ignore
        )

    @staticmethod
    async def refresh_token(*, refresh_payload: TokenPayload = Depends(security.refresh_token_required)) -> GetNewToken:
        access_token = security.create_access_token(refresh_payload.sub)
        date_now = datetime.now()

        return GetNewToken(
            access_token=access_token, access_token_expire_time=date_now + security.config.JWT_ACCESS_TOKEN_EXPIRES
        )


auth_service = AuthService()

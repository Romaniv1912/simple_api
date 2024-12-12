#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime

from src.app.schema.user import GetUserInfoNoRelationDetails
from src.common.schema import SchemaBase


class AccessTokenBase(SchemaBase):
    access_token: str
    access_token_type: str = 'Bearer'
    access_token_expire_time: datetime


class RefreshTokenBase(SchemaBase):
    refresh_token: str
    refresh_token_type: str = 'Bearer'
    refresh_token_expire_time: datetime


class GetNewToken(AccessTokenBase):
    pass


class GetLoginToken(AccessTokenBase, RefreshTokenBase):
    user: GetUserInfoNoRelationDetails

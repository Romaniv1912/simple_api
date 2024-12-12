from fastapi import APIRouter, Depends

from src.app.service.auth import GetLoginToken, GetNewToken, auth_service

router = APIRouter()


@router.post('/new', summary='Get token', description='Login user into service')
def new(data: GetLoginToken = Depends(auth_service.new_token)) -> GetLoginToken:
    return data


@router.post('/refresh', summary='Refresh token', description='Refresh user token')
def refresh(data: GetNewToken = Depends(auth_service.refresh_token)) -> GetNewToken:
    return data

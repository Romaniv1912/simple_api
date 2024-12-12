from fastapi import APIRouter

from src.app.schema.ping import GetPing

router = APIRouter()


@router.get('/ping', summary='Ping', description='Allow to ping service')
def ping() -> GetPing:
    return GetPing()

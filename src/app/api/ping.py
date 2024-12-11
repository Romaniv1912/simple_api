from fastapi import APIRouter

from src.app.schema.ping import GetPing

route = APIRouter()


@route.get('/ping', summary='Ping', description='Allow to ping service')
def ping() -> GetPing:
    return GetPing()

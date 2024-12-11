from fastapi import APIRouter

from src.app.schema.ping import GetPing

route = APIRouter()


@route.get('/ping',
           summary='Ping service',
           description='Allow to ping service')
def ping() -> GetPing:
    return GetPing()

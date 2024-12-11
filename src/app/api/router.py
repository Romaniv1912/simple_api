from fastapi import APIRouter

from src.app.api.ping import route as ping_route

route = APIRouter()

route.include_router(ping_route)

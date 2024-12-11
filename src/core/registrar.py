from fastapi import FastAPI

from src.app.api.router import route
from src.core.conf import settings
from src.utils.health_check import ensure_unique_route_names
from src.utils.openapi import simplify_operation_ids


def register_app():
    # FastAPI
    app = FastAPI(
        title=settings.APP.TITLE,
        version=settings.APP.VERSION,
        description=settings.APP.DESCRIPTION,
        docs_url=settings.APP.DOCS_URL,
        redoc_url=settings.APP.REDOCS_URL,
        openapi_url=settings.APP.OPENAPI_URL,
        root_path=settings.APP.BASE_PATH,
    )

    # routing
    register_router(app)

    return app


def register_router(app: FastAPI):
    """
    Routing

    :param app: FastAPI
    :return:
    """

    # API
    app.include_router(route)

    # Extra
    ensure_unique_route_names(app)
    simplify_operation_ids(app)

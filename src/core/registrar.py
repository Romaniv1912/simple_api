from fastapi import FastAPI

from src.app.api.router import route
from src.core.conf import settings, LOG_DIR
from src.utils.health_check import ensure_unique_route_names
from src.utils.logs import setup_logging, set_customize_logfile
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

    # journal
    register_logger()

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


def register_logger() -> None:
    """
    system log

    :return:
    """
    setup_logging(settings.LOG)
    set_customize_logfile(LOG_DIR, settings.LOG)
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src.app.api.router import router
from src.common.security import security
from src.core.conf import LOG_DIR, settings
from src.utils.health_check import ensure_unique_route_names
from src.utils.logs import set_customize_logfile, setup_logging
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

    register_logger()
    register_exception(app)
    register_router(app)
    register_page(app)

    return app


def register_router(app: FastAPI):
    """
    Routing

    :param app: FastAPI
    :return:
    """

    # API
    app.include_router(router)

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


def register_exception(app: FastAPI):
    """
    Register Exception

    :param app:
    :return:
    """

    # Register AuthX exceptions
    security.handle_errors(app)


def register_page(app: FastAPI):
    """
    Page query

    :param app:
    :return:
    """
    add_pagination(app)

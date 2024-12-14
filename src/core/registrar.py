from contextlib import asynccontextmanager
from uuid import uuid4

from asgi_correlation_id import CorrelationIdMiddleware
from asgi_correlation_id.middleware import is_valid_uuid4
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src.app.api.router import router
from src.common.security import security
from src.core.conf import LOG_DIR, settings
from src.database import create_table
from src.utils.health_check import ensure_unique_route_names
from src.utils.logs import set_customize_logfile, setup_logging
from src.utils.openapi import simplify_operation_ids


@asynccontextmanager
async def register_init(app: FastAPI):
    """
    Start initialization

    :return:
    """

    # Create database table
    await create_table()

    yield


def register_app():
    """
    Create FastAPI app

    :return:
    """
    app = FastAPI(
        title=settings.APP.TITLE,
        version=settings.APP.VERSION,
        description=settings.APP.DESCRIPTION,
        docs_url=settings.APP.DOCS_URL,
        redoc_url=settings.APP.REDOCS_URL,
        openapi_url=settings.APP.OPENAPI_URL,
        root_path=settings.APP.BASE_PATH,
        lifespan=register_init,
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


def register_middleware(app: FastAPI):
    """
    Middleware, execution order from bottom to top

    :param app:
    :return:
    """
    # Trace ID (required)
    app.add_middleware(
        CorrelationIdMiddleware,  # type: ignore
        update_request_header=True,
        header_name=settings.APP.TRACE_ID_REQUEST_HEADER_KEY,
        generator=lambda: uuid4().hex,
        validator=is_valid_uuid4,
        transformer=lambda a: a,
    )

    # CORS: Always at the end
    if settings.APP.MIDDLEWARE_CORS:
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,  # type: ignore
            allow_origins=settings.APP.CORS_ALLOWED_ORIGINS,
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
            expose_headers=settings.APP.CORS_EXPOSE_HEADERS,
        )

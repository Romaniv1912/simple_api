from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """App Settings"""

    model_config = SettingsConfigDict(env_prefix='APP_')

    # FastAPI
    TITLE: str
    VERSION: str
    DESCRIPTION: str
    DOCS_URL: str | None = None
    REDOCS_URL: str | None = None
    OPENAPI_URL: str | None = None
    BASE_PATH: str

    PREFIX: str

    # Trace ID
    TRACE_ID_REQUEST_HEADER_KEY: str = 'X-Request-ID'

    # CORS Setting
    MIDDLEWARE_CORS: bool = True
    CORS_ALLOWED_ORIGINS: tuple[str] = ('*',)
    CORS_EXPOSE_HEADERS: tuple[str] = (TRACE_ID_REQUEST_HEADER_KEY,)


class CerbosSettings(BaseSettings):
    """Database Settings"""

    model_config = SettingsConfigDict(env_prefix='CERBOS_')

    HTTP_HOST: str = 'localhost'
    HTTP_PORT: int = 5432

    @property
    def http_url(self):
        return f'http://{self.HTTP_HOST}:{self.HTTP_PORT}'


class DatabaseSettings(BaseSettings):
    """Database Settings"""

    model_config = SettingsConfigDict(env_prefix='POSTGRES_')

    ECHO: bool = False
    SCHEMA: str = 'postgresql+asyncpg'
    HOST: str = 'localhost'
    PORT: int = 5432
    DB: str
    USER: str
    PASSWORD: str

    @property
    def url(self) -> str:
        return f'{self.SCHEMA}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}'


class LogSettings(BaseSettings):
    """Logs Settings"""

    model_config = SettingsConfigDict(env_prefix='LOG_')

    ROOT_LEVEL: str = 'NOTSET'
    STD_FORMAT: str = (
        '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</> | <lvl>{level: <8}</> | '
        '<cyan> {correlation_id} </> | <lvl>{message}</>'
    )
    LOGURU_FORMAT: str = (
        '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</> | <lvl>{level: <8}</> | '
        '<cyan> {correlation_id} </> | <lvl>{message}</>'
    )
    CID_DEFAULT_VALUE: str = '-'
    CID_UUID_LENGTH: int = 32  # must <= 32
    STDOUT_LEVEL: str = 'INFO'
    STDERR_LEVEL: str = 'ERROR'
    STDOUT_FILENAME: str = 'api_access.log'
    STDERR_FILENAME: str = 'api_error.log'

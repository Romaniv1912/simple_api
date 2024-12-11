from pydantic_settings import BaseSettings, SettingsConfigDict


class TokenSettings(BaseSettings):
    """Token Settings"""

    model_config = SettingsConfigDict(env_prefix='TOKEN_')

    SECRET_KEY: str  # Key secrets.token_urlsafe(32)
    ALGORITHM: str = 'HS256'  # algorithm
    EXPIRE_SECONDS: int = 60 * 60 * 24 * 1  # expiration time unit seconds
    PREFIX: str


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

import os

from functools import lru_cache
from os.path import join
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from src.common.settings import AppSettings, CerbosSettings, DatabaseSettings, LogSettings

# Get the project root directory
# Or use an absolute path to the backend directory
BASE_PATH = Path(__file__).resolve().parent.parent.parent

# Log file path
LOG_DIR = os.path.join(BASE_PATH, 'logs')

load_dotenv(join(BASE_PATH, '.env.prod'))
load_dotenv(join(BASE_PATH, '.env'), override=True)


class Settings(BaseSettings):
    """Global Settings"""

    # Env Config
    ENVIRONMENT: Literal['dev', 'pro']

    APP: AppSettings = AppSettings()
    DB: DatabaseSettings = DatabaseSettings()
    CERBOS: CerbosSettings = CerbosSettings()
    LOG: LogSettings = LogSettings()


@lru_cache
def get_settings() -> Settings:
    """Get global configuration"""
    return Settings()


# Create configuration instance
settings = get_settings()

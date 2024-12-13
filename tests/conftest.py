from os.path import join
from typing import Generator

import pytest
from dotenv import load_dotenv

from starlette.testclient import TestClient

from main import app
from src.core.conf import settings, BASE_PATH


load_dotenv(join(BASE_PATH, '.env.test'), override=True)


@pytest.fixture(scope='module')
def client() -> Generator:
    with TestClient(app, root_path=settings.APP.BASE_PATH) as c:
        yield c

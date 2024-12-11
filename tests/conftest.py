from typing import Generator

import pytest

from starlette.testclient import TestClient

from main import app
from src.core.conf import settings


@pytest.fixture(scope='module')
def client() -> Generator:
    with TestClient(app, root_path=settings.APP.BASE_PATH) as c:
        yield c

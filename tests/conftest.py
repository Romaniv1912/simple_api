from typing import Dict, Generator

import pytest

from starlette.testclient import TestClient

from main import app
from src.core.conf import settings
from tests.types import Users
from tests.utils import get_token_headers


@pytest.fixture(scope='module')
def client() -> Generator:
    with TestClient(app, root_path=settings.APP.BASE_PATH) as c:
        yield c


@pytest.fixture(scope='module')
def headers(client: TestClient) -> Dict[str, Dict[str, str]]:
    return {user: get_token_headers(client, user) for user in Users.all()}

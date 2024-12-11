from starlette.testclient import TestClient

from src.core.conf import settings


def test_ping(client: TestClient) -> None:
    resp = client.get(f"{settings.APP.BASE_PATH}/ping")

    assert resp.status_code == 200, 'Bad status code'
    assert resp.json() == {'ping': 'pong'}, 'Response is not a pong response'
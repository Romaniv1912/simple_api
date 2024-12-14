import pytest

from starlette.testclient import TestClient

from tests.types import Users


def test_ping(client: TestClient) -> None:
    resp = client.get('/ping')

    assert resp.status_code == 200, 'Bad status code'
    assert resp.json() == {'ping': 'pong'}, 'Response is not a pong response'


@pytest.mark.parametrize('username', Users.all())
def test_auth(username, client: TestClient, headers) -> None:
    resp = client.get('/users/me', headers=headers[username])

    user = resp.json()

    assert user['username'] == username, 'Username is not ' + username

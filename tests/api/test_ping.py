from starlette.testclient import TestClient


def test_ping(client: TestClient) -> None:
    resp = client.get('/ping')

    assert resp.status_code == 200, 'Bad status code'
    assert resp.json() == {'ping': 'pong'}, 'Response is not a pong response'

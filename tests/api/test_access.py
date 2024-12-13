import pytest
from starlette.testclient import TestClient

from tests.types import Users, Records


@pytest.mark.parametrize(
    'username,record,expected',
    [
        (Users.ADMIN, Records.ADMIN, 200),
        (Users.ADMIN, Records.USER1, 200),
        (Users.MANAGER, Records.USER1, 403),
        (Users.MANAGER, Records.USER2, 200),
        (Users.USER1, Records.USER2, 403),
        (Users.USER1, Records.USER1, 200),
    ]
)
def test_single_access(username, record, expected, client: TestClient, headers):
    resp = client.get(f'/records/{record}', headers=headers[username])

    assert resp.status_code == expected, 'Access rule failed'
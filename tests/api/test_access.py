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
def test_single_record_access(username, record, expected, client: TestClient, headers):
    resp = client.get(f'/records/{record}', headers=headers[username])

    assert resp.status_code == expected, 'Access rule failed'


@pytest.mark.parametrize(
    'username,expected',
    [
        (Users.ADMIN, [Users.ADMIN_ID, Users.MANAGER_ID, Users.USER1_ID, Users.USER2_ID]),
        (Users.MANAGER, [Users.MANAGER_ID, Users.USER2_ID]),
        (Users.USER1, [Users.USER1_ID]),
        (Users.USER2, [Users.USER2_ID]),
    ]
)
def test_multiple_record_access(username, expected, client: TestClient, headers):
    resp = client.get(f'/records', headers=headers[username])

    assert resp.status_code == 200, 'Access forbidden'

    items = resp.json()['items']

    assert len(items) >= 1, 'Wrong number of records'

    assert all(map(lambda x: int(x['user_id']) in expected, items)), 'Access rule failed'
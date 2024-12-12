from starlette.testclient import TestClient


def get_token_headers(client: TestClient, username: str) -> dict[str, str]:
    response = client.post(
        '/auth/new',
        params={
            'username': username,
            'password': 'password',
        },
    )

    response.raise_for_status()
    token_type = response.json()['access_token_type']
    access_token = response.json()['access_token']
    headers = {'Authorization': f'{token_type} {access_token}'}
    return headers

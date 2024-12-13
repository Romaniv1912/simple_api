from starlette.testclient import TestClient

def get_token_headers(client: TestClient, username: str) -> dict[str, str]:
    response = client.post(
        '/token/new',
        json={
            'username': username,
            'password': 'password',
        },
    )

    data = response.json()
    token_type = data['access_token_type']
    access_token = data['access_token']
    headers = {'Authorization': f'{token_type} {access_token}'}
    return headers

from http import HTTPStatus

from chat.utils.http_utils import parse_content


def test_non_existent(fake_id, client):
    response = client.get(f"/users/{fake_id}/")
    content = parse_content(response)

    assert content == {"error": f"User does not exist. ID: {fake_id}"}
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_success(user_1, client):
    response = client.get(f"/users/{user_1.id}/")

    assert response.status_code == HTTPStatus.OK

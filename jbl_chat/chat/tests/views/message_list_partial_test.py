from http import HTTPStatus

from chat.utils.http_utils import parse_content


def test_sender_user_non_existent(user_recipient, fake_id, client):
    response = client.get(f"/messages/partials/{fake_id}/{user_recipient.id}/")
    content = parse_content(response)

    assert content == {"error": f"User does not exist. ID: {fake_id}"}
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_recipient_user_non_existent(user_sender, fake_id, client):
    response = client.get(f"/messages/partials/{user_sender.id}/{fake_id}/")
    content = parse_content(response)

    assert content == {"error": f"User does not exist. ID: {fake_id}"}
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_no_messages(user_sender, user_recipient, client):
    response = client.get(f"/messages/partials/{user_sender.id}/{user_recipient.id}/")

    assert response.status_code == HTTPStatus.OK


def test_only_sender_messages(user_sender, user_recipient, message_1, message_2, client):
    response = client.get(f"/messages/partials/{user_sender.id}/{user_recipient.id}/")

    assert response.status_code == HTTPStatus.OK


def test_only_recipient_messages(
    user_sender,
    user_recipient,
    message_3,
    message_4,
    client,
):
    response = client.get(f"/messages/partials/{user_sender.id}/{user_recipient.id}/")

    assert response.status_code == HTTPStatus.OK


def test_sender_and_recipient_messages(  # noqa: PLR0913
    user_sender,
    user_recipient,
    message_1,
    message_2,
    message_3,
    message_4,
    client,
):
    response = client.get(f"/messages/partials/{user_sender.id}/{user_recipient.id}/")

    assert response.status_code == HTTPStatus.OK


def test_swap_sender_and_recipient_returns_same_result(
    user_sender,
    user_recipient,
    client,
):
    response_1 = client.get(f"/messages/partials/{user_sender.id}/{user_recipient.id}/")
    response_2 = client.get(f"/messages/partials/{user_recipient.id}/{user_sender.id}/")

    assert response_1.status_code == HTTPStatus.OK
    assert response_2.status_code == HTTPStatus.OK

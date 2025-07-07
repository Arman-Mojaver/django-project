from http import HTTPStatus

from chat.models import Message
from chat.utils.http_utils import parse_content


def test_sender_user_non_existent(user_recipient, fake_id, client):
    data = {"content": "some content"}
    response = client.post(
        f"/message/partials/{fake_id}/{user_recipient.id}/",
        data=data,
    )
    content = parse_content(response)

    assert content == {"error": f"User does not exist. ID: {fake_id}"}
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_recipient_user_non_existent(user_sender, fake_id, client):
    data = {"content": "some content"}
    response = client.post(
        f"/message/partials/{user_sender.id}/{fake_id}/",
        data=data,
    )
    content = parse_content(response)

    assert content == {"error": f"User does not exist. ID: {fake_id}"}
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_invalid_content(user_sender, user_recipient, client):
    data = {}
    response = client.post(
        f"/message/partials/{user_sender.id}/{user_recipient.id}/",
        data=data,
        content_type="application/json",
    )
    content = parse_content(response)

    assert content == {"error": "Invalid content: None"}
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_message(user_sender, user_recipient, message_data_1, client):
    data = {"content": message_data_1["content"]}
    response = client.post(
        f"/message/partials/{user_sender.id}/{user_recipient.id}/",
        data=data,
    )

    db_message = Message.objects.first()

    assert db_message.content == message_data_1["content"]
    assert db_message.recipient_id == message_data_1["recipient_id"]
    assert db_message.sender_id == message_data_1["sender_id"]

    assert response.status_code == HTTPStatus.OK


def test_same_user_raises_error(user_sender, message_data_1, client):
    data = {"content": message_data_1["content"]}
    response = client.post(
        f"/message/partials/{user_sender.id}/{user_sender.id}/",
        data=data,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

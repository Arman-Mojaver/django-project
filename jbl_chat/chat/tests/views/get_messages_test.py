from chat.utils.http_utils import parse_content
from rest_framework.fields import DateTimeField


def test_sender_user_non_existent(user_recipient, fake_id, client):
    response = client.get(f"/api/messages/{fake_id}/{user_recipient.id}/")
    content = parse_content(response)

    assert content == {"error": f"Sender user does not exist. ID: {fake_id}"}


def test_recipient_user_non_existent(user_sender, fake_id, client):
    response = client.get(f"/api/messages/{user_sender.id}/{fake_id}/")
    content = parse_content(response)

    assert content == {"error": f"Recipient user does not exist. ID: {fake_id}"}


def test_no_messages(user_sender, user_recipient, client):
    response = client.get(f"/api/messages/{user_sender.id}/{user_recipient.id}/")
    content = parse_content(response)

    assert content == {"data": []}


def test_only_sender_messages(user_sender, user_recipient, message_1, message_2, client):
    response = client.get(f"/api/messages/{user_sender.id}/{user_recipient.id}/")
    content = parse_content(response)

    expected_messages = [
        {
            "content": message_1.content,
            "created_at": DateTimeField().to_representation(message_1.created_at),
            "id": message_1.id,
            "recipient_id": message_1.recipient_id,
            "sender_id": message_1.sender_id,
        },
        {
            "content": message_2.content,
            "created_at": DateTimeField().to_representation(message_2.created_at),
            "id": message_2.id,
            "recipient_id": message_2.recipient_id,
            "sender_id": message_2.sender_id,
        },
    ]

    assert content == {"data": expected_messages}


def test_only_recipient_messages(
    user_sender,
    user_recipient,
    message_3,
    message_4,
    client,
):
    response = client.get(f"/api/messages/{user_sender.id}/{user_recipient.id}/")
    content = parse_content(response)

    expected_messages = [
        {
            "content": message_3.content,
            "created_at": DateTimeField().to_representation(message_3.created_at),
            "id": message_3.id,
            "recipient_id": message_3.recipient_id,
            "sender_id": message_3.sender_id,
        },
        {
            "content": message_4.content,
            "created_at": DateTimeField().to_representation(message_4.created_at),
            "id": message_4.id,
            "recipient_id": message_4.recipient_id,
            "sender_id": message_4.sender_id,
        },
    ]

    assert content == {"data": expected_messages}


def test_sender_and_recipient_messages(  # noqa: PLR0913
    user_sender,
    user_recipient,
    message_1,
    message_2,
    message_3,
    message_4,
    client,
):
    response = client.get(f"/api/messages/{user_sender.id}/{user_recipient.id}/")
    content = parse_content(response)

    expected_messages = [
        {
            "content": message_1.content,
            "created_at": DateTimeField().to_representation(message_1.created_at),
            "id": message_1.id,
            "recipient_id": message_1.recipient_id,
            "sender_id": message_1.sender_id,
        },
        {
            "content": message_2.content,
            "created_at": DateTimeField().to_representation(message_2.created_at),
            "id": message_2.id,
            "recipient_id": message_2.recipient_id,
            "sender_id": message_2.sender_id,
        },
        {
            "content": message_3.content,
            "created_at": DateTimeField().to_representation(message_3.created_at),
            "id": message_3.id,
            "recipient_id": message_3.recipient_id,
            "sender_id": message_3.sender_id,
        },
        {
            "content": message_4.content,
            "created_at": DateTimeField().to_representation(message_4.created_at),
            "id": message_4.id,
            "recipient_id": message_4.recipient_id,
            "sender_id": message_4.sender_id,
        },
    ]

    assert content == {"data": expected_messages}


def test_swap_sender_and_recipient_returns_same_result(
    user_sender,
    user_recipient,
    client,
):
    response_1 = client.get(f"/api/messages/{user_sender.id}/{user_recipient.id}/")
    content_1 = parse_content(response_1)

    response_2 = client.get(f"/api/messages/{user_recipient.id}/{user_sender.id}/")
    content_2 = parse_content(response_2)

    assert content_1 == content_2

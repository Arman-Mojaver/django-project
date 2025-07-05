import json

import pytest
from chat.models import Message, User
from chat.utils.http_utils import parse_content
from rest_framework.fields import DateTimeField

NON_EXISTENT_USER_ID = 12345678


@pytest.fixture
def user_sender_data():
    return {"fullname": "User Usersson", "email": "userusersson@mail.com"}


@pytest.fixture
def user_recipient_data():
    return {"fullname": "User Usersson2", "email": "userusersson2@mail.com"}


@pytest.fixture
def user_sender(user_sender_data):
    user = User(**user_sender_data)
    user.save()
    return user


@pytest.fixture
def user_recipient(user_recipient_data):
    user = User(**user_recipient_data)
    user.save()
    return user


@pytest.fixture
def message_data_1(user_sender, user_recipient):
    return {
        "content": "Hello, how are you?",
        "sender_id": user_sender.id,
        "recipient_id": user_recipient.id,
    }


def test_sender_user_non_existent(user_recipient, client):
    data = {"content": "some content"}
    response = client.post(
        f"/message/{NON_EXISTENT_USER_ID}/{user_recipient.id}/",
        data=data,
    )
    content = parse_content(response)

    assert content == {"error": f"Sender user does not exist. ID: {NON_EXISTENT_USER_ID}"}


def test_recipient_user_non_existent(user_sender, client):
    data = {"content": "some content"}
    response = client.post(
        f"/message/{user_sender.id}/{NON_EXISTENT_USER_ID}/",
        data=data,
    )
    content = parse_content(response)

    assert content == {
        "error": f"Recipient user does not exist. ID: {NON_EXISTENT_USER_ID}"
    }


def test_invalid_content(user_sender, user_recipient, client):
    data = {}
    response = client.post(
        f"/message/{user_sender.id}/{user_recipient.id}/",
        data=json.dumps(data),
        content_type="application/json",
    )
    content = parse_content(response)

    assert content == {"error": "Invalid content: None"}


def test_create_message(user_sender, user_recipient, message_data_1, client):
    data = {"content": message_data_1["content"]}
    response = client.post(
        f"/message/{user_sender.id}/{user_recipient.id}/",
        data=json.dumps(data),
        content_type="application/json",
    )
    content = parse_content(response)
    message = content["data"]

    assert message["content"] == message_data_1["content"]
    assert message["recipient_id"] == message_data_1["recipient_id"]
    assert message["sender_id"] == message_data_1["sender_id"]

    db_message = Message.objects.first()

    assert db_message.content == message["content"]
    assert db_message.recipient_id == message["recipient_id"]
    assert db_message.sender_id == message["sender_id"]
    assert db_message.id == message["id"]
    assert (
        DateTimeField().to_representation(db_message.created_at) == message["created_at"]
    )

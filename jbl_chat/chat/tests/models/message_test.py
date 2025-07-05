import pytest
from chat.models import Message, User


@pytest.fixture
def user_data_sender():
    return {"fullname": "Sender Person", "email": "sender@mail.com"}


@pytest.fixture
def user_data_recipient():
    return {"fullname": "Recipient Person", "email": "recipient@mail.com"}


@pytest.fixture
def user_sender(user_data_sender):
    user = User(**user_data_sender)
    user.save()
    return user


@pytest.fixture
def user_recipient(user_data_recipient):
    user = User(**user_data_recipient)
    user.save()
    return user


@pytest.fixture
def message_data(user_sender, user_recipient):
    return {
        "content": "Hello, how are you?",
        "sender_id": user_sender.id,
        "recipient_id": user_recipient.id,
    }


@pytest.fixture
def message_1(message_data):
    return Message.objects.create(
        content=message_data["content"],
        sender_id=message_data["sender_id"],
        recipient_id=message_data["recipient_id"],
    )


def test_create_message(message_data):
    Message.objects.create(
        content=message_data["content"],
        sender_id=message_data["sender_id"],
        recipient_id=message_data["recipient_id"],
    )

    expected_message = {
        "content": message_data["content"],
        "sender_id": message_data["sender_id"],
        "recipient_id": message_data["recipient_id"],
    }
    message = Message.objects.first()

    assert message.content == expected_message["content"]
    assert message.sender_id == expected_message["sender_id"]
    assert message.recipient_id == expected_message["recipient_id"]
    assert message.created_at


def test_get_message(message_1, message_data):
    expected = {
        "content": message_data["content"],
        "sender_id": message_data["sender_id"],
        "recipient_id": message_data["recipient_id"],
    }
    assert message_1.content == expected["content"]
    assert message_1.sender_id == expected["sender_id"]
    assert message_1.recipient_id == expected["recipient_id"]
    assert message_1.created_at


def test_update_message(message_1, message_data):
    message_1.content = "New content!"
    message_1.save()

    expected = {
        "content": "New content!",
        "sender_id": message_data["sender_id"],
        "recipient_id": message_data["recipient_id"],
    }

    assert message_1.content == expected["content"]
    assert message_1.sender_id == expected["sender_id"]
    assert message_1.recipient_id == expected["recipient_id"]
    assert message_1.created_at


def test_delete_message(message_1):
    message_1.delete()

    assert list(Message.objects.all()) == []


def test_cascade_delete_on_sender(message_1, user_sender):
    user_sender.delete()
    assert list(Message.objects.all()) == []


def test_cascade_delete_on_recipient(message_1, user_recipient):
    user_recipient.delete()
    assert list(Message.objects.all()) == []

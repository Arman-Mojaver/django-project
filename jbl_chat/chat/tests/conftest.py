import os
import sys
from pathlib import Path

import django
import pytest
from django.core.management import call_command
from django.test import Client

sys.path.append(Path(__file__).resolve().parent.parent.parent.as_posix())

os.environ["ENVIRONMENT"] = "testing"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jbl_chat.jbl_chat.settings")

from config import config as project_config

if not project_config.is_testing():
    err = f"Invalid testing environment: {project_config}"


django.setup()

from chat.models import Message, User  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def django_cleanup_and_migrate():
    call_command("flush", interactive=False)
    call_command("migrate", interactive=False)


@pytest.fixture(autouse=True)
def flush_db_before_test():
    call_command("flush", interactive=False)


@pytest.fixture
def client():
    return Client()


# User data fixtures


@pytest.fixture
def user_data_1():
    return {"fullname": "User Usersson", "email": "userusersson@mail.com"}


@pytest.fixture
def user_data_2():
    return {"fullname": "User Usersson2", "email": "userusersson2@mail.com"}


@pytest.fixture
def user_data_3():
    return {"fullname": "User Usersson3", "email": "userusersson3@mail.com"}


@pytest.fixture
def user_sender_data(user_data_1):
    return user_data_1


@pytest.fixture
def user_recipient_data(user_data_2):
    return user_data_2


# User fixtures


@pytest.fixture
def user_1(user_data_1):
    user = User(**user_data_1)
    user.save()
    return user


@pytest.fixture
def user_2(user_data_2):
    user = User(**user_data_2)
    user.save()
    return user


@pytest.fixture
def user_3(user_data_3):
    user = User(**user_data_3)
    user.save()
    return user


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


# Message data fixtures


@pytest.fixture
def message_data_1(user_sender, user_recipient):
    return {
        "content": "Hello, how are you?",
        "sender_id": user_sender.id,
        "recipient_id": user_recipient.id,
    }


@pytest.fixture
def message_data_2(user_sender, user_recipient):
    return {
        "content": "Hello?",
        "sender_id": user_sender.id,
        "recipient_id": user_recipient.id,
    }


@pytest.fixture
def message_data_3(user_sender, user_recipient):
    return {
        "content": "Hi.",
        "sender_id": user_sender.id,
        "recipient_id": user_recipient.id,
    }


@pytest.fixture
def message_data_4(user_sender, user_recipient):
    return {
        "content": "Bye",
        "sender_id": user_sender.id,
        "recipient_id": user_recipient.id,
    }


# Message fixtures


@pytest.fixture
def message_1(message_data_1):
    return Message.objects.create(
        content=message_data_1["content"],
        sender_id=message_data_1["sender_id"],
        recipient_id=message_data_1["recipient_id"],
    )


@pytest.fixture
def message_2(message_data_2):
    return Message.objects.create(
        content=message_data_2["content"],
        sender_id=message_data_2["sender_id"],
        recipient_id=message_data_2["recipient_id"],
    )


@pytest.fixture
def message_3(message_data_3):
    return Message.objects.create(
        content=message_data_3["content"],
        sender_id=message_data_3["recipient_id"],
        recipient_id=message_data_3["sender_id"],
    )


@pytest.fixture
def message_4(message_data_4):
    return Message.objects.create(
        content=message_data_4["content"],
        sender_id=message_data_4["recipient_id"],
        recipient_id=message_data_4["sender_id"],
    )


# Other fixtures
@pytest.fixture
def fake_id():
    """Non existent id in the DB."""
    return 12345678

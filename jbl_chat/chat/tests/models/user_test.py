import pytest
from chat.models import User
from django.db.utils import IntegrityError


@pytest.fixture
def user_data_1():
    return {"fullname": "User Usersson", "email": "userusersson@mail.com"}


@pytest.fixture
def user_1(user_data_1):
    user = User(**user_data_1)
    user.save()

    return user


def test_create_user(user_data_1):
    user = User(**user_data_1)
    user.save()

    user_db = User.objects.first()

    assert user_db.fullname == user_data_1["fullname"]
    assert user_db.email == user_data_1["email"]


def test_get_user(user_1, user_data_1):
    user_db = User.objects.first()

    assert user_db.fullname == user_data_1["fullname"]
    assert user_db.email == user_data_1["email"]


def test_update_user(user_1, user_data_1):
    modified_user_data_1 = {**user_data_1}
    modified_user_data_1["fullname"] = "modified fullname"

    user_1.fullname = "modified fullname"
    user_1.save()

    user_db = User.objects.first()

    assert user_db.fullname == modified_user_data_1["fullname"]
    assert user_db.email == modified_user_data_1["email"]


def test_delete_user(user_1):
    user_1.delete()

    assert list(User.objects.all()) == []


def test_user_email_is_unique(user_1, user_data_1):
    user = User(fullname="Another name", email=user_data_1["email"])

    with pytest.raises(IntegrityError):
        user.save()

import pytest
from chat.models import User
from chat.utils.http_utils import parse_content

NON_EXISTENT_USER_ID = 12345678


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


def test_non_existent(client):
    response = client.get(f"/users/{NON_EXISTENT_USER_ID}/")
    content = parse_content(response)

    assert content == {"error": f"User does not exist. ID: {NON_EXISTENT_USER_ID}"}


def test_one_user(user_1, client):
    response = client.get(f"/users/{user_1.id}/")
    content = parse_content(response)

    assert content == {"data": []}


def test_two_users(user_1, user_2, user_data_2, client):
    response = client.get(f"/users/{user_1.id}/")
    content = parse_content(response)

    expected_users = [
        {
            "email": "userusersson2@mail.com",
            "fullname": "User Usersson2",
            "id": user_2.id,
        },
    ]

    assert content == {"data": expected_users}


def test_several_users(user_1, user_data_1, user_2, user_3, user_data_3, client):  # noqa: PLR0913
    response = client.get(f"/users/{user_2.id}/")
    content = parse_content(response)

    expected_users = [
        {
            "email": user_data_1["email"],
            "fullname": user_data_1["fullname"],
            "id": user_1.id,
        },
        {
            "email": user_data_3["email"],
            "fullname": user_data_3["fullname"],
            "id": user_3.id,
        },
    ]

    assert content == {"data": expected_users}

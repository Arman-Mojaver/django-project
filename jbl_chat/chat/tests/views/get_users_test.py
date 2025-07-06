from chat.utils.http_utils import parse_content


def test_non_existent(fake_id, client):
    response = client.get(f"/api/users/{fake_id}/")
    content = parse_content(response)

    assert content == {"error": f"User does not exist. ID: {fake_id}"}
    assert response.status_code == 404


def test_one_user(user_1, client):
    response = client.get(f"/api/users/{user_1.id}/")
    content = parse_content(response)

    assert content == {"data": []}
    assert response.status_code == 200


def test_two_users(user_1, user_2, user_data_2, client):
    response = client.get(f"/api/users/{user_1.id}/")
    content = parse_content(response)

    expected_users = [
        {
            "email": "userusersson2@mail.com",
            "fullname": "User Usersson2",
            "id": user_2.id,
        },
    ]

    assert content == {"data": expected_users}
    assert response.status_code == 200


def test_several_users(user_1, user_data_1, user_2, user_3, user_data_3, client):  # noqa: PLR0913
    response = client.get(f"/api/users/{user_2.id}/")
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
    assert response.status_code == 200

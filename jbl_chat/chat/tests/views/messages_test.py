def test_non_existent_user(fake_id, user_2, client):
    response = client.get(f"/messages/{fake_id}/{user_2.id}/")

    assert response.status_code == 404


def test_non_existent_other_user(user_1, fake_id, client):
    response = client.get(f"/messages/{user_1.id}/{fake_id}/")

    assert response.status_code == 404


def test_same_user_raises_error(user_1, client):
    response = client.get(f"/messages/{user_1.id}/{user_1.id}/")

    assert response.status_code == 422


def test_success(user_1, user_2, client):
    response = client.get(f"/messages/{user_1.id}/{user_2.id}/")

    assert response.status_code == 200

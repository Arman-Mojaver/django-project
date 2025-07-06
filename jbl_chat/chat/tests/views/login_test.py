def test_success(client):
    response = client.get("/login/")

    assert response.status_code == 200

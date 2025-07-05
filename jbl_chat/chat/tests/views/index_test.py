from chat.utils.http_utils import parse_content


def test_index(client):
    response = client.get("/")
    content = parse_content(response)
    assert content == {"message": "Server Working!"}

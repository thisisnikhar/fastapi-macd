def test_home(client, auth_headers):
    response = client.get(
        "/macd/",
        headers=auth_headers
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data["message"] == "This is home from MACD router"


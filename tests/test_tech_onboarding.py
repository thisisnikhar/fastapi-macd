def test_create_request(client,auth_headers):
    response = client.post(
        "/techonboarding/request",
        headers=auth_headers,
        json={
            "tech_data": [
                {
                    "ip_address": "strings",
                    "tech_type": "Database",
                    "tech_name": "string",
                    "tech_version": "string"
                }
            ]
        }
    )

    data = response.json()
    assert response.status_code == 201
    assert data["ticket_id"] == 1
    assert data["request_data"] == {
        "tech_data": [
            {
                "ip_address": "strings",
                "tech_type": "Database",
                "tech_name": "string",
                "tech_version": "string"
            }
        ]
    }


def test_get_all_tech_requests_data_current_user(client,auth_headers):
    # creating a ticket
    client.post(
        "/techonboarding/request",
        headers=auth_headers,
        json={
            "tech_data": [
                {
                    "ip_address": "strings",
                    "tech_type": "Database",
                    "tech_name": "string",
                    "tech_version": "string"
                }
            ]
        }
    )

    # getting the tickets
    response = client.get(
        "/techonboarding/my-requests",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()

    request = data["data"][0]
    assert request["ticket_type"] == "tech"
    assert request["username"] == "userone"
    assert request["user_email"] == "userone@test.com"

    tech_data = request["server_data"][0]
    assert tech_data["ip_address"] == "strings"
    assert tech_data["tech_type"] == "Database"
    assert tech_data["tech_name"] == "string"
    assert tech_data["tech_version"] == "string"

    assert len(data["data"]) == 1


def test_get_all_tech_requests_data(client,admin_headers):
    # creating a ticket
    client.post(
        "/techonboarding/request",
        headers=admin_headers,
        json={
            "tech_data": [
                {
                    "ip_address": "strings",
                    "tech_type": "Database",
                    "tech_name": "string",
                    "tech_version": "string"
                }
            ]
        }
    )

    # getting the tickets
    response = client.get(
        "/techonboarding/",
        headers=admin_headers,
    )
    data = response.json()

    request = data["data"][0]
    assert request["ticket_type"] == "tech"
    assert request["username"] == "admin"
    assert request["user_email"] == "admin@test.com"

    tech_data = request["server_data"][0]
    assert tech_data["ip_address"] == "strings"
    assert tech_data["tech_type"] == "Database"
    assert tech_data["tech_name"] == "string"
    assert tech_data["tech_version"] == "string"

    assert len(data["data"]) == 1


def test_get_all_tech_requests_data_negative(client,auth_headers):
    # creating a ticket
    client.post(
        "/techonboarding/request",
        headers=auth_headers,
        json={
            "tech_data": [
                {
                    "ip_address": "strings",
                    "tech_type": "Database",
                    "tech_name": "string",
                    "tech_version": "string"
                }
            ]
        }
    )

    # getting the tickets
    response = client.get(
        "/techonboarding/",
        headers=auth_headers,
    )
    data = response.json()
    assert data["detail"] == "This feature is applicable only for admins"
    assert response.status_code == 403

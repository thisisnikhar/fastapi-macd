def test_create_request(client,auth_headers):
    response = client.post(
        "/cionboarding/request",
        headers=auth_headers,
        json={
              "server_data": [
                {
                  "ip_address": "strings",
                  "hostname": "string",
                  "serial_number": "string",
                  "operating_system": "string",
                  "os_version": "string",
                  "cpu": 1,
                  "memory": 1,
                  "hard_disk": 1
                }
              ]
            }
    )
    data = response.json()
    assert response.status_code == 201
    assert data["ticket_id"] == 1
    assert data["request_data"] == {
            "server_data": [
                {
                    "ip_address": "strings",
                    "hostname": "string",
                    "serial_number": "string",
                    "operating_system": "string",
                    "os_version": "string",
                    "cpu": 1,
                    "memory": 1,
                    "hard_disk": 1
                }
            ]
        }


def test_get_all_ci_requests_data(client,admin_headers):
    # creating a ticket
    client.post(
        "/cionboarding/request",
        headers=admin_headers,
        json={
            "server_data": [
                {
                    "ip_address": "10.10.10.10",
                    "hostname": "string",
                    "serial_number": "string",
                    "operating_system": "string",
                    "os_version": "string",
                    "cpu": 1,
                    "memory": 1,
                    "hard_disk": 1
                }
            ]
        }
    )
    # getting the tickets
    response = client.get(
        "/cionboarding/",
        headers=admin_headers,
    )
    assert response.status_code == 200
    data = response.json()

    request = data["data"][0]
    assert request["ticket_type"] == "ci"
    assert request["username"] == "admin"
    assert request["user_email"] == "admin@test.com"

    server_data = request["server_data"][0]

    assert server_data["ip_address"] == "10.10.10.10"
    assert server_data["hostname"] == "string"
    assert server_data["serial_number"] == "string"
    assert server_data["cpu"] == 1
    assert server_data["memory"] == 1
    assert server_data["hard_disk"] == 1

    assert len(data["data"]) == 1


def test_get_all_ci_requests_data_current_user(client,auth_headers):
    # creating a ticket
    client.post(
        "/cionboarding/request",
        headers=auth_headers,
        json={
            "server_data": [
                {
                    "ip_address": "10.10.10.10",
                    "hostname": "string",
                    "serial_number": "string",
                    "operating_system": "string",
                    "os_version": "string",
                    "cpu": 1,
                    "memory": 1,
                    "hard_disk": 1
                }
            ]
        }
    )

    # getting the tickets
    response = client.get(
        "/cionboarding/my-requests",
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()

    request = data["data"][0]
    assert request["ticket_type"] == "ci"
    assert request["username"] == "userone"
    assert request["user_email"] == "userone@test.com"

    server_data = request["server_data"][0]

    assert server_data["ip_address"] == "10.10.10.10"
    assert server_data["hostname"] == "string"
    assert server_data["serial_number"] == "string"
    assert server_data["cpu"] == 1
    assert server_data["memory"] == 1
    assert server_data["hard_disk"] == 1

    assert len(data["data"]) == 1

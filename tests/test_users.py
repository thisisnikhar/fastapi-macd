from commons.auth import get_current_user

from commons.db_dependency import db_dependency


def test_get_all_usernames(client,admin_headers):
    # Create a test user
    create_response = client.post(
        "/users",
        headers=admin_headers,
        json = {
            "username": "test_user",
            "email": "test_user@email.com",
            "password": "stringst",
            "role": "user"
        }
    )
    assert create_response.status_code == 201

    response = client.get(
        "/users",
        headers=admin_headers
    )
    data = response.json()
    assert response.status_code == 200
    assert len(data["username_list"]) > 0
    assert "test_user" in data["username_list"]


def test_create_user_and_login(client,admin_headers,test_db):
    # Create a user
    create_response = client.post(
        "/users",
        headers=admin_headers,
        json={
            "username": "test_user",
            "email": "test_user@email.com",
            "password": "stringst",
            "role": "user"
        }
    )
    assert create_response.status_code == 201

    # Testing a login
    login_response = client.post(
        "/users/login",
        data={
            "username": "test_user",
            "password": "stringst"
        }
    )
    data = login_response.json()
    assert login_response.status_code == 200
    assert "access_token" in data
    assert data["access_token"] is not None
    assert data["token_type"] == "bearer"

    current_user = get_current_user(
        db=test_db,
        token=data["access_token"]
    )

    assert current_user.username == "test_user"


def test_create_user_and_login_negative(client,admin_headers):
    # Create a user
    create_response = client.post(
        "/users",
        headers=admin_headers,
        json={
            "username": "test_user",
            "email": "test_user@email.com",
            "password": "wrong_password",
            "role": "user"
        }
    )
    assert create_response.status_code == 201

    # Testing a login
    login_response = client.post(
        "/users/login",
        data={
            "username": "test_user",
            "password": "stringst"
        }
    )
    data = login_response.json()

    assert login_response.status_code == 401
    assert data["detail"] == "Invalid username or password"



def test_create_user(client,admin_headers,test_db):
    # Create a test user
    create_response = client.post(
        "/users",
        headers=admin_headers,
        json = {
            "username": "new_user",
            "email": "new_user@email.com",
            "password": "new_user_password",
            "role": "user"
        }
    )
    assert create_response.status_code == 201

    response = client.post(
        "/users/login",
        data={
            "username": "new_user",
            "password": "new_user_password"
        }
    )
    data = response.json()
    print(data)
    assert response.status_code == 200
    assert "access_token" in data
    assert data["access_token"] is not None
    assert data["token_type"] == "bearer"
    # assert "new_user" in data["username_list"]

    current_user = get_current_user(
        db=test_db,
        token=data["access_token"]
    )

    assert current_user.username == "new_user"
    assert current_user.email == "new_user@email.com"
    assert current_user.role == "user"
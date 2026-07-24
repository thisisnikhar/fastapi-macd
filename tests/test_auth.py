from datetime import timedelta

from commons.auth import create_access_token, get_current_user
from tests.conftest import TestingSessionLocal


# def test_login(client,auth_headers):
#     assert auth_headers["Authorization"].startswith("Bearer")
#

def test_current_user(test_user):
    db = TestingSessionLocal()
    user = test_user

    token = create_access_token(
        user=user,
        expires_delta=timedelta(minutes=30)
    )
    current_user = get_current_user(
        db=db,
        token=token["access_token"]
    )
    assert current_user.username == "userone"
    assert current_user.email == "userone@test.com"
    assert current_user.role == "user"

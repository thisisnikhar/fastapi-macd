from main import app
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

from commons.database import base
from commons.db_dependency import get_db
from commons.models import Users, RequestData, CIOnboardingServerData, TechOnboardingServerData

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Admin%40123@localhost/macd_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_user():
    db = TestingSessionLocal()

    # Delete child tables first
    db.query(CIOnboardingServerData).delete()
    db.query(TechOnboardingServerData).delete()
    db.query(RequestData).delete()
    db.query(Users).delete()
    db.commit()

    # Remove existing user if present
    db.query(Users).filter(
        Users.username == "userone"
    ).delete()

    db.commit()

    user = Users(
        username="userone",
        email="userone@test.com",
        password=bcrypt_context.hash("test1234"),
        role="user"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    yield user

    # Cleanup
    db.query(CIOnboardingServerData).delete()
    db.query(TechOnboardingServerData).delete()
    db.query(RequestData).delete()
    db.query(Users).delete()
    db.commit()
    db.close()


@pytest.fixture
def auth_headers(client, test_user):
    response = client.post(
        "/users/login",
        data={
            "username": "userone",
            "password": "test1234"
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


@pytest.fixture
def admin_user():
    db = TestingSessionLocal()

    # Cleanup
    db.query(CIOnboardingServerData).delete()
    db.query(TechOnboardingServerData).delete()
    db.query(RequestData).delete()
    db.query(Users).delete()
    db.commit()

    user = Users(
        username="admin",
        email="admin@test.com",
        password=bcrypt_context.hash("admin123"),
        role="admin"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    yield user

    # Cleanup
    db.query(CIOnboardingServerData).delete()
    db.query(TechOnboardingServerData).delete()
    db.query(RequestData).delete()
    db.query(Users).delete()
    db.commit()
    db.close()


@pytest.fixture
def admin_headers(client, admin_user):
    response = client.post(
        "/users/login",
        data={
            "username": "admin",
            "password": "admin123"
        }
    )

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }
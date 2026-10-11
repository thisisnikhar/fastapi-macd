from datetime import timedelta, datetime, timezone
import os

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from passlib.context import CryptContext

from commons.db_dependency import db_dependency
from commons.models import Users


load_dotenv("local.env")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/users/login")

bcrypt_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120")
)


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(Users).filter(Users.username == username).first()

    if user is None:
        return None

    if not bcrypt_context.verify(password, user.password):
        return None

    return user


def create_access_token(user: Users, expires_delta: timedelta):
    expire = datetime.now(timezone.utc) + expires_delta

    payload = {
        "sub": user.username,
        "id": user.id,
        "exp": expire
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# Validate the user
def get_current_user(
    db: db_dependency,
    token: str = Depends(oauth2_bearer)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")
        user_id = payload.get("id")

        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

        user = db.query(Users).filter(Users.id == user_id).first()

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
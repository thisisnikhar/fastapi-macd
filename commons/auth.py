from datetime import timedelta,datetime,timezone

from fastapi import Depends,HTTPException
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status

from commons.db_dependency import db_dependency
from commons.models import Users
from passlib.context import CryptContext

from fastapi.security import OAuth2PasswordBearer

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/users/login")

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated="auto")


SECRET_KEY = "bbbd584d00268f7c8064753498b237a3aaf4adb9633d4ac3e2aa3b4d22a49043"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120


def authenticate_user(username: str, password: str,db:Session):
    user = db.query(Users).filter(Users.username==username).first()
    if user is None:
        return None
    if not bcrypt_context.verify(password,user.password):
        return None
    return user


def create_access_token(user:Users, expires_delta: timedelta):
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {
        "sub": user.username,
        "id": user.id,
        "exp": expire
    }
    token = jwt.encode(
        payload,
        SECRET_KEY,
        ALGORITHM
    )
    return {
        "access_token": token,
        "token_type": "bearer"
    }


# Validate the user
def get_current_user(db:db_dependency,token: str = Depends(oauth2_bearer)):
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
        user = db.query(Users).filter(Users.id==user_id).first()

        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Could not validate credentials"
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
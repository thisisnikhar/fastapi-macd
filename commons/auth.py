from sqlalchemy.orm import Session

from commons.models import Users
from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated="auto")


def authenticate_user(username: str, password: str,db:Session):
    user = db.query(Users).filter(Users.username==username).first()
    if user is None:
        return None
    if not bcrypt_context.verify(password,user.password):
        return None
    return user
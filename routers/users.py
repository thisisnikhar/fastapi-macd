from fastapi import APIRouter,Depends
from typing import Annotated

from sentry_sdk import session

from commons.database import SessionLocal
from sqlalchemy.orm import Session
from commons.models import Users
from sqlalchemy import select,or_,func
from commons.pydantic_models import User

users_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session,Depends(get_db)]


@users_router.get("/",summary="Get all Usernames")
async def get_all_usernames(db:db_dependency):
    stmt = select(Users.username)

    data =  db.execute(stmt).mappings().all()
    username_list = [item["username"] for item in data]
    return {"username_list":username_list}


@users_router.post("/",summary="Create a user")
async def create_user(db:db_dependency,user:User):
    query = select(func.max(Users.id))
    max_user_id = db.execute(query).scalar()
    if max_user_id is None:
        new_id = 1
    else:
        new_id = int(max_user_id) + 1
    new_user = Users(
        id = new_id,
        username = user.username,
        password = user.password,
        email = user.email,
        role = user.role
    )
    results = db.query(Users).filter(
        or_(
            Users.username==user.username,
            Users.email==user.email
        )
    ).all()
    data = list(results)
    print(data)
    if len(data) == 0:
        #Add user
        db.add(new_user)
        db.commit()
        return "User added"
    if data[0].username == user.username:
        return "User already exists with the given username"
    if data[0].email == user.email:
        return "User already exists with the given email"
    db.add(new_user)
    db.commit()
    return "User added successfully"

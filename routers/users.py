from fastapi import APIRouter,Depends
from typing import Annotated
from commons.database import SessionLocal
from sqlalchemy.orm import Session
from commons.models import Users
from sqlalchemy import select

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
    return db.execute(stmt).mappings().all()
from fastapi import APIRouter,Depends
from passlib.context import CryptContext
from commons.models import Users
from sqlalchemy import select,or_,func
from commons.pydantic_models import User, Authenticate
from commons.db_dependency import db_dependency
from commons.auth import authenticate_user

users_router = APIRouter()



bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

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
        password = bcrypt_context.hash(user.password),
        email = user.email,
        role = user.role
    )
    results = db.query(Users).filter(
        or_(
            Users.username==user.username,
            Users.email==user.email
        )
    ).first()
    data = list(results)
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


@users_router.post("/check_authentication",summary="Checking if authentication works")
async def check_authentication(db:db_dependency,user:Authenticate):
    authenticated_user = authenticate_user(
        username=user.username,
        password=user.password,
        db=db
    )
    if authenticated_user is None:
        return {
            "authenticated": False,
            "message": "Invalid username or password"
        }
    else:
        return {
            "authenticated": True,
            "id": authenticated_user.id,
            "username": authenticated_user.username,
            "email": authenticated_user.email,
            "role": authenticated_user.role
        }
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from starlette import status

from commons.models import Users
from sqlalchemy import select,or_,func
from commons.pydantic_models import User
from commons.db_dependency import db_dependency
from commons.auth import authenticate_user, create_access_token, get_current_user

users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

@users_router.get("/",summary="Get all Usernames")
async def get_all_usernames(db:db_dependency,current_user=Depends(get_current_user)):
    if current_user:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You are not an admin"
            )

        stmt = select(Users.username)

        data =  db.execute(stmt).mappings().all()
        username_list = [item["username"] for item in data]
        return {"username_list":username_list}
    else:
        raise HTTPException(
            status=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized"
        )


@users_router.post("/",summary="Create a user")
async def create_user(db:db_dependency,user:User,current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not an admin"
        )
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
    if results is None:
        #Add user
        db.add(new_user)
        db.commit()
        return "User added"
    data = list(results)
    if data[0].username == user.username:
        return "User already exists with the given username"
    if data[0].email == user.email:
        return "User already exists with the given email"
    db.add(new_user)
    db.commit()
    return "User added successfully"


@users_router.post("/login",summary="Create Access Token")
async def login(db:db_dependency,form_data: OAuth2PasswordRequestForm = Depends()):
    authenticated_user = authenticate_user(
        username=form_data.username,
        password=form_data.password,
        db=db
    )
    if authenticated_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    else:
        token = create_access_token(
            authenticated_user,
            timedelta(minutes=30)
        )
        return token
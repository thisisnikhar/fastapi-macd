from pydantic import BaseModel, Field
from typing import Literal


class User(BaseModel):
    username: str = Field(min_length=5,max_length=20)
    email: str = Field(min_length=5,max_length=100)
    password: str = Field(min_length=8,max_length=20)
    role: Literal["user","admin"] # Only "user" and "admin" roles are allowed


class Authenticate(BaseModel):
    username: str = Field(min_length=5)
    password: str = Field(min_length=5)
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


class ServerData(BaseModel):
    ip_address: str = Field(min_length=7,max_length=80)
    hostname: str = Field(min_length=3,max_length=80)
    serial_number: str = Field(min_length=3,max_length=80)
    operating_system: str = Field(min_length=3, max_length=80)
    os_version: str = Field(min_length=1,max_length=80)
    cpu: int = Field(lt=1000,gt=0)
    memory: int = Field(lt=100_000,gt=0)
    hard_disk: int = Field(lt=10000,gt=0)


class CIOnboardingRequest(BaseModel):
    ticket_type: str = Literal["ci"]
    server_data: list[ServerData]

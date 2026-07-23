from pydantic import BaseModel, Field
from typing import Literal


class User(BaseModel):
    username: str = Field(min_length=5,max_length=20)
    email: str = Field(min_length=5,max_length=100)
    password: str = Field(min_length=8,max_length=20)
    role: Literal["user","admin","ticket_admin"]
    # Only "user", "ticket_admin" and "admin" roles are allowed


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
    server_data: list[ServerData]


class StatusUpdate(BaseModel):
    status: Literal["Open","In Progress","Closed"]


class TechData(BaseModel):
    ip_address: str = Field(min_length=7,max_length=80)
    tech_type: Literal["Database", "Middleware"]
    tech_name: str = Field(min_length=3,max_length=30)
    tech_version: str = Field(min_length=1,max_length=15)


class TechOnboardingRequest(BaseModel):
    tech_data: list[TechData]


# Defining response models
class CIServerResponse(BaseModel):
    record_id: int
    ip_address: str
    hostname: str
    serial_number: str
    operating_system: str
    os_version: str
    cpu: int
    memory: int
    hard_disk: int


class CIResponse(BaseModel):
    ticket_number: str
    ticket_type: str
    username: str
    user_email: str
    server_data: list[CIServerResponse]


class CIResponseList(BaseModel):
    data: list[CIResponse]


class TechServerResponse(BaseModel):
    record_id: int
    ip_address: str
    tech_type: str
    tech_name: str
    tech_version: str


class TechResponse(BaseModel):
    ticket_number: str
    ticket_type: str
    username: str
    user_email: str
    server_data: list[TechServerResponse]


class TechResponseList(BaseModel):
    data: list[TechResponse]
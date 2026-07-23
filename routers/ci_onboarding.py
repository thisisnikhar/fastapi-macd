from datetime import datetime
from ipaddress import ip_address

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from commons.models import RequestData,CIOnboardingServerData,Users
from commons.db_dependency import db_dependency
from commons.auth import get_current_user
from commons.pydantic_models import CIOnboardingRequest,StatusUpdate
from sqlalchemy import select,or_,func


ci_onboarding_router = APIRouter()


@ci_onboarding_router.get("/",summary="Get all the CI Onboarding Requests",status_code=status.HTTP_200_OK)
async def get_all_ci_requests_data(db:db_dependency,current_user=Depends(get_current_user)):
    if current_user.role not in ["admin","ticket_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="This feature is applicable only for admins")
    requests = db.query(RequestData).filter(RequestData.ticket_type=="ci").all()
    response = []
    for req in requests:
        server_data = []
        for server in req.ci_onboarding:
            server_data.append(
                {
                    "record_id": server.record_id,
                    "ip_address": server.ip_address,
                    "hostname": server.hostname,
                    "serial_number": server.serial_number,
                    "operating_system": server.operating_system,
                    "os_version": server.os_version,
                    "cpu": server.cpu,
                    "memory": server.memory,
                    "hard_disk": server.hard_disk
                }
            )
        response.append(
            {
                "ticket_number": req.ticket_number,
                "ticket_type": req.ticket_type,
                "username": req.users.username,
                "user_email": req.users.email,
                "server_data": server_data
            }
        )
    return {"data": response}


@ci_onboarding_router.post("/request",status_code=status.HTTP_201_CREATED)
async def create_request(request_data:CIOnboardingRequest,db:db_dependency,current_user=Depends(get_current_user)):
    query = select(func.max(RequestData.ticket_id))
    max_ticket_id = db.execute(query).scalar()
    if max_ticket_id is None:
        ticket_id = 1
    else:
        ticket_id = int(max_ticket_id) + 1
    year = datetime.now().strftime("%y")  # 26
    ticket_number = f"SR-{year}-{ticket_id:05d}"
    # return request_data.ticket_type
    # Updating RequestData table
    request = RequestData(
        ticket_id=ticket_id,
        ticket_number=ticket_number,
        ticket_type = "ci",
        user_id = current_user.id,
        status = "In Progress"
    )
    db.add(request)
    db.commit()

    query = select(func.max(CIOnboardingServerData.id))
    max_id = db.execute(query).scalar()
    if max_id is None:
        new_id = 1
    else:
        new_id = int(max_id) + 1

    server_data = request_data.server_data
    record_id = 1
    for data in server_data:
        data = data.model_dump() # JSON Request Data to dictionary

        # Updating CIOnboardingServerData Table
        ci_onboarding_server_data = CIOnboardingServerData(
            id=new_id,
            record_id=record_id,
            ip_address=data.get("ip_address"),
            hostname=data.get("hostname"),
            serial_number = data.get("serial_number"),
            operating_system = data.get("operating_system"),
            os_version = data.get("os_version"),
            cpu = data.get("cpu"),
            memory = data.get("memory"),
            hard_disk = data.get("hard_disk"),
            request_id = ticket_number
        )
        db.add(ci_onboarding_server_data)
        new_id = new_id + 1
        record_id = record_id + 1
    db.commit()

    return {"ticket_id":ticket_id,"request_data":request_data}


@ci_onboarding_router.get("/my-requests",summary="Get the CI Onboarding Requests for the current user",status_code=status.HTTP_200_OK)
async def get_all_ci_requests_data_current_user(db:db_dependency,
                                                current_user=Depends(get_current_user)):
    requests = db.query(RequestData).filter(RequestData.ticket_type=="ci",
                                            RequestData.user_id==current_user.id).all()
    response = []
    for req in requests:
        server_data = []
        for server in req.ci_onboarding:
            server_data.append(
                {
                    "record_id": server.record_id,
                    "ip_address": server.ip_address,
                    "hostname": server.hostname,
                    "serial_number": server.serial_number,
                    "operating_system": server.operating_system,
                    "os_version": server.os_version,
                    "cpu": server.cpu,
                    "memory": server.memory,
                    "hard_disk": server.hard_disk
                }
            )
        response.append(
            {
                "ticket_number": req.ticket_number,
                "ticket_type": req.ticket_type,
                "username": req.users.username,
                "user_email": req.users.email,
                "server_data": server_data
            }
        )
    return {"data": response}


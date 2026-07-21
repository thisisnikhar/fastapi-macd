from datetime import datetime
from ipaddress import ip_address

from fastapi import APIRouter, Depends
from commons.models import RequestData,CIOnboardingServerData
from commons.db_dependency import db_dependency
from commons.auth import get_current_user
from commons.pydantic_models import CIOnboardingRequest
from sqlalchemy import select,or_,func


ci_onboarding_router = APIRouter()


@ci_onboarding_router.get("/",summary="Get all the CI Onboarding Requests")
async def get_all_ci_requests(db:db_dependency,current_user=Depends(get_current_user)):
    return db.query(RequestData).all()


@ci_onboarding_router.post("/request")
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
        ticket_type = request_data.ticket_type,
        user_id = current_user.id
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
    print(server_data)
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

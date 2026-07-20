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

    # Updating CIOnboardingServerData Table
    ci_onboarding_server_data = CIOnboardingServerData(
        id=1,
        record_id=1,
        ip_address=request_data.ip_address,
        hostname=request_data.hostname,
        serial_number = request_data.serial_number,
        operating_system = request_data.operating_system,
        os_version = request_data.os_version,
        cpu = request_data.cpu,
        memory = request_data.memory,
        hard_disk = request_data.hard_disk
    )
    db.add(ci_onboarding_server_data)
    db.commit()

    return {"ticket_id":ticket_id,"request_data":request_data}

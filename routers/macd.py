from fastapi import APIRouter, Depends, HTTPException
from commons.user_dependency import current_user_dependency
from commons.pydantic_models import StatusUpdate
from commons.db_dependency import db_dependency
from commons.auth import get_current_user
from starlette import status
from commons.models import RequestData


macd_router = APIRouter()



@macd_router.get("/")
async def home(current_user=current_user_dependency):
    return {"message": "This is home from MACD router"}


@macd_router.patch("/request/{ticket_number}",summary="Update the status of an existing ticket",status_code=status.HTTP_200_OK)
async def update_ticket_status(request_data:StatusUpdate,
                               db:db_dependency,
                               ticket_number:str,
                               current_user=current_user_dependency):
    if current_user.role != "ticket_admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="This feature is applicable only for Ticket Admins")
    ticket = db.query(RequestData).filter(
        RequestData.ticket_number == ticket_number
    ).first()
    if ticket is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found"
        )

    ticket.status = request_data.status
    ticket.status_updated_by = current_user.username
    db.add(ticket)
    db.commit()
    return {
              "message": "Ticket status updated successfully",
              "ticket_number": ticket_number,
              "status": request_data.status,
              "status_updated_by": current_user.username
            }


@macd_router.get("/request/{ticket_number}",summary="Fetch a particular ticket",status_code=status.HTTP_200_OK)
async def get_ticket_details(ticket_number:str,
                                db:db_dependency,
                                current_user = current_user_dependency):
    ticket_data = db.query(RequestData).filter(
        RequestData.ticket_number == ticket_number
    ).first()

    ticket_response = {
        "ticket_number": ticket_data.ticket_number,
        "ticket_type": ticket_data.ticket_type,
        "status": ticket_data.status,
        "status_updated_by": ticket_data.status_updated_by,
        "username": ticket_data.users.username,
        "user_email": ticket_data.users.email,
    }

    if ticket_data.ticket_type == "ci":
        server_data = []
        for server in ticket_data.ci_onboarding:
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
        ticket_response["server_data"] = server_data
    else:
        tech_data = []
        for tech in ticket_data.tech_onboarding:
            tech_data.append(
                {
                    "record_id": tech.record_id,
                    "ip_address": tech.ip_address,
                    "tech_type": tech.tech_type,
                    "tech_name": tech.tech_name,
                    "tech_version": tech.tech_version,
                }
            )
        ticket_response["tech_data"] = tech_data

    return ticket_response
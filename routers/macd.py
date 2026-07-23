from fastapi import APIRouter, Depends, HTTPException
from commons.auth import get_current_user
from commons.pydantic_models import StatusUpdate
from commons.db_dependency import db_dependency
from commons.auth import get_current_user
from starlette import status
from commons.models import RequestData


macd_router = APIRouter()



@macd_router.get("/")
async def home(current_user=Depends(get_current_user)):
    return {"message": "This is home from MACD router"}


@macd_router.patch("/request/{ticket_number}",summary="Update the status of an existing ticket",status_code=status.HTTP_200_OK)
async def update_ticket_status(request_data:StatusUpdate,
                               db:db_dependency,
                               ticket_number:str,
                               current_user=Depends(get_current_user)):
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

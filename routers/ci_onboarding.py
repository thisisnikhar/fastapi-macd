from fastapi import APIRouter, HTTPException
from starlette import status

from commons.models import RequestData
from commons.db_dependency import db_dependency
from commons.user_dependency import current_user_dependency
from commons.pydantic_models import CIOnboardingRequest,CIResponseList
from commons.utilities import (add_ci_onboarding_server_data,generate_new_ticket_id_and_ticket_number,
                               generate_ci_response_data)


ci_onboarding_router = APIRouter()


@ci_onboarding_router.get("/",summary="Get all the CI Onboarding Requests",status_code=status.HTTP_200_OK,response_model=CIResponseList)
async def get_all_ci_requests_data(db:db_dependency,current_user=current_user_dependency):
    if current_user.role not in ["admin","ticket_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="This feature is applicable only for admins")
    requests = db.query(RequestData).filter(RequestData.ticket_type=="ci").all()
    response = generate_ci_response_data(requests)

    return {"data": response}


@ci_onboarding_router.post("/request",status_code=status.HTTP_201_CREATED)
async def create_request(request_data:CIOnboardingRequest,db:db_dependency,current_user=current_user_dependency):
    ticket_id,ticket_number = generate_new_ticket_id_and_ticket_number(db)
    # Updating RequestData table
    request = RequestData(
        ticket_id=ticket_id,
        ticket_number=ticket_number,
        ticket_type = "ci",
        user_id = current_user.id,
        status = "In Progress"
    )
    db.add(request)
    # Updating server data
    server_data = request_data.server_data
    add_ci_onboarding_server_data(server_data,db,ticket_number)

    db.commit()

    return {"ticket_id":ticket_id,"request_data":request_data}


@ci_onboarding_router.get("/my-requests",summary="Get the CI Onboarding Requests for the current user",status_code=status.HTTP_200_OK,response_model=CIResponseList)
async def get_all_ci_requests_data_current_user(db:db_dependency,
                                                current_user=current_user_dependency):
    requests = db.query(RequestData).filter(RequestData.ticket_type=="ci",
                                            RequestData.user_id==current_user.id).all()
    response = generate_ci_response_data(requests)
    return {"data": response}


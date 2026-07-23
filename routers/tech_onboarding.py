from fastapi import APIRouter,HTTPException
from starlette import status
from commons.db_dependency import db_dependency
from commons.models import RequestData
from commons.pydantic_models import TechOnboardingRequest,TechResponseList
from commons.user_dependency import current_user_dependency
from commons.utilities import generate_new_ticket_id_and_ticket_number,add_tech_onboarding_server_data,generate_tech_response_data


tech_onboarding_router = APIRouter()


@tech_onboarding_router.get("/",summary="Get all the Tech Onboarding Requests",status_code=status.HTTP_200_OK,response_model=TechResponseList)
async def get_all_tech_requests_data(db: db_dependency,current_user=current_user_dependency):
    if current_user.role not in ["admin","ticket_admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="This feature is applicable only for admins")
    requests = db.query(RequestData).filter(RequestData.ticket_type == "tech").all()
    response = generate_tech_response_data(requests)
    return {"data": response}


@tech_onboarding_router.post("/request",status_code=status.HTTP_201_CREATED)
async def create_request(request_data:TechOnboardingRequest,db:db_dependency,current_user=current_user_dependency):
    ticket_id,ticket_number = generate_new_ticket_id_and_ticket_number(db)

    # Updating RequestData table
    request = RequestData(
        ticket_id=ticket_id,
        ticket_number=ticket_number,
        ticket_type = "tech",
        user_id = current_user.id,
        status = "In Progress"
    )
    db.add(request)

    # Updating tech data
    tech_data = request_data.tech_data
    add_tech_onboarding_server_data(tech_data,ticket_number,db)
    db.commit()

    return {"ticket_id":ticket_id,"request_data":request_data}


@tech_onboarding_router.get("/my-requests",summary="Get the Tech Onboarding Requests for the current user",status_code=status.HTTP_200_OK,response_model=TechResponseList)
async def get_all_tech_requests_data_current_user(db:db_dependency,
                                                current_user=current_user_dependency):
    requests = db.query(RequestData).filter(RequestData.ticket_type=="tech",
                                            RequestData.user_id==current_user.id).all()
    response = generate_tech_response_data(requests)
    return {"data": response}
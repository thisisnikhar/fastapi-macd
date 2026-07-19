from fastapi import APIRouter
from commons.models import RequestData
from commons.db_dependency import db_dependency


ci_onboarding_router = APIRouter()


@ci_onboarding_router.get("/",summary="Get all the CI Onboarding Requests")
async def get_all_ci_requests(db:db_dependency):
    return db.query(RequestData).all()



@ci_onboarding_router.post("/request")
async def create_request(db:db_dependency):
    return "This is not ready yet"

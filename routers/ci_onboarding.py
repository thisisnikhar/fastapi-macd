from fastapi import APIRouter, Depends
from commons.models import RequestData
from commons.db_dependency import db_dependency
from commons.auth import get_current_user


ci_onboarding_router = APIRouter()


@ci_onboarding_router.get("/",summary="Get all the CI Onboarding Requests")
async def get_all_ci_requests(db:db_dependency,current_user=Depends(get_current_user)):
    return db.query(RequestData).all()


@ci_onboarding_router.post("/request")
async def create_request(db:db_dependency,current_user=Depends(get_current_user)):
    return "This is not ready yet"

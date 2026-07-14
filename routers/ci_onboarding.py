from fastapi import APIRouter, Depends
from commons.models import CIOnboardingServerData
from commons.database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from commons.models import RequestData,CIOnboardingServerData


ci_onboarding_router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session,Depends(get_db)]

@ci_onboarding_router.get("/",summary="Get all the CI Onboarding Requests")
async def get_all_ci_requests(db:db_dependency):
    return db.query(RequestData).all()

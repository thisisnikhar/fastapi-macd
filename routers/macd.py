from fastapi import APIRouter, Depends
from commons.auth import get_current_user


macd_router = APIRouter()


@macd_router.get("/")
async def home(current_user=Depends(get_current_user)):
    return {"message": "This is home from MACD router"}

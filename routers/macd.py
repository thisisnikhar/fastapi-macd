from fastapi import APIRouter


macd_router = APIRouter()


@macd_router.get("/")
async def home():
    return {"message": "This is home from MACD router"}

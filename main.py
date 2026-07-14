from fastapi import FastAPI
from routers.macd import macd_router
from routers.ci_onboarding import ci_onboarding_router


app = FastAPI()

app.include_router(
    macd_router,
    prefix="/macd",
    tags=["Main Module"]
)

app.include_router(
    ci_onboarding_router,
    prefix="/cionboarding",
    tags=["CI Onboarding"]
)

from fastapi import APIRouter
from app.samplelogin.views import router

API_STR = "/api"

login_router = APIRouter(prefix=API_STR)
login_router.include_router(router)

from fastapi import APIRouter
from app.books.views import router

API_STR = "/api"

books_router = APIRouter(prefix=API_STR)
books_router.include_router(router)
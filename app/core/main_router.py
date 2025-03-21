from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.books import books_router  
from app.samplelogin import router as samplelogin_router  

router = APIRouter()

# Include the books and samplelogin routers
router.include_router(books_router)
router.include_router(samplelogin_router)

@router.get("/healthcheck", status_code=200)
def healthcheck():
    return JSONResponse(content=jsonable_encoder({"status": "Healthy yayy!"}))

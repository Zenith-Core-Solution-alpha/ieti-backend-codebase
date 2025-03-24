import os
from fastapi import FastAPI, APIRouter, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi_sqlalchemy import DBSessionMiddleware
from dotenv import load_dotenv

from app.sneakers import sneakers_router
from app.core.main_router import router as main_router
from app.core.logger import init_logging

load_dotenv(".env")

root_router = APIRouter()

app = FastAPI(title="FastAPI Boiler Plate")
app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])

# ✅ Add routers
app.include_router(main_router)
app.include_router(sneakers_router)
app.include_router(root_router)

# ✅ Exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        field = ".".join(error["loc"])
        message = error["msg"]
        errors.append({"field": field, "message": message})
    
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": errors},
    )

# ✅ Initialize logging
init_logging()

if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")

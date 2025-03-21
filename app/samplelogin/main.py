import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.samplelogin.views import router as login_router  # Import the router

load_dotenv('.env')

app = FastAPI()

# Register the sample login router
app.include_router(login_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI Sample Login!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

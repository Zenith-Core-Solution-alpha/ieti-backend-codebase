import uvicorn
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.books.views import router as book_router  # Import the router

load_dotenv('.env')

app = FastAPI()

# Register the books router (which contains authors too)
app.include_router(book_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Hello, world!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

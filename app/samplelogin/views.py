from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.samplelogin.models import User as UserModel
from app.samplelogin.schema import UserSchema
from loguru import logger
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

router = APIRouter()

# User registrations

@router.post("/register", status_code=201)
async def register_user(payload: UserSchema, db: Session = Depends(get_db)):

    existing_user = db.query(UserModel).filter(
        (UserModel.username == payload.username) | (UserModel.email == payload.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already taken")

    new_user = UserModel(
        username=payload.username,
        email=payload.email,
        password=payload.password,  # Ideally, hash the password before storing it
        birthdate=payload.birthdate,
         status="pending" 
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.success("User registered with pending status.")
    return {
        "message": "Registration submitted. Awaiting approval.",
        "user": {
            "username": new_user.username,
            "email": new_user.email,
            "status": new_user.status
        }
    }

# User Login

@router.post("/login", status_code=200)
async def login_user(payload: UserSchema, db: Session = Depends(get_db)):
    """
    Logs in the user only if they are approved.
    """
    user = db.query(UserModel).filter(UserModel.username == payload.username).first()

    if not user or user.password != payload.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if user.status != "approved":
        raise HTTPException(status_code=403, detail="Your account is not approved yet. Please wait for registrar approval.")

    return {
        "message": "Login successful",
        "user": {
            "username": user.username,
            "email": user.email,
            "status": user.status
        }
    }


@router.put("/approve/{user_id}", status_code=200)
async def approve_user(user_id: int, status: str, db: Session = Depends(get_db)):
    """
    Approves or rejects a pending user.
    """
    if status not in ["approved", "pending"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.status == "approved":
        raise HTTPException(status_code=400, detail="User is already approved")

    user.status = status
    db.commit()

    return {
        "message": f"User status updated to {status}",
        "user": {
            "id": user.id,
            "username": user.username,
            "status": user.status
        }
    }
@router.get("/users", status_code=200)
async def list_users(status: str = "all", db: Session = Depends(get_db)):
    """
    List users with optional status filtering.
    """
    query = db.query(UserModel)

    if status in ["pending", "approved"]:
        query = query.filter(UserModel.status == status)

    users = query.all()

    return {
        "users": [{"id": u.id, "username": u.username, "status": u.status} for u in users]
    }

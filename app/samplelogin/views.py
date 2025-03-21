from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db.session import get_db
from app.samplelogin.models import User as UserModel
from app.samplelogin.schema import UserSchema
from loguru import logger

router = APIRouter()

# -------------------------------
# Register User
# -------------------------------
@router.post("/register", status_code=201)
async def register_user(payload: UserSchema, db: Session = Depends(get_db)):
    """
    Registers a new user in the database.

    Returns:
        Object: The registered user details.
    """
    # Check if the username already exists
    existing_user = db.query(UserModel).filter(UserModel.username == payload.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = UserModel(
        username=payload.username,
        password=payload.password  # Ideally, hash the password before storing it
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    logger.success("User registered successfully.")
    return {"message": "User registered successfully", "user": new_user.username}


# -------------------------------
# User Login
# -------------------------------
@router.post("/login", status_code=200)
async def login_user(payload: UserSchema, db: Session = Depends(get_db)):
    """
    Logs in the user by verifying the username and password.

    Returns:
        Object: Success message or error.
    """
    user = db.query(UserModel).filter(UserModel.username == payload.username).first()

    if not user or user.password != payload.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    logger.success("User logged in successfully.")
    return {"message": "Login successful", "user": user.username}

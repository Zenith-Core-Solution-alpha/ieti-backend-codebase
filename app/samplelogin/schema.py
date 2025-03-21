from pydantic import BaseModel, Field

# -------------------------------
# User Schema
# -------------------------------
class UserSchema(BaseModel):
    username: str = Field(..., example="user123")
    password: str = Field(..., example="securepassword")

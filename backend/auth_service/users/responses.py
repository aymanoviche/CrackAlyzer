from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from bson import ObjectId

class BaseResponse(BaseModel):
    class Config:
        from_attriubte = True
        arbitrary_types_allowed = True

class UserResponse(BaseModel):
    id: str  # Define id as a string
    full_name: str
    username: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        json_encoders = {
            ObjectId: str  # Convert ObjectId to string
        }
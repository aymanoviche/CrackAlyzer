from pydantic import BaseModel, Field, EmailStr, validator # basemodel: Serialization (easy to convert model instances back to JSON or dictionaries) , validation(ensures input matches types)  , and Data Parsing (converts input data to Python objects)
from datetime import datetime
from typing import Optional
from bson import ObjectId
import hashlib
import re

class UserModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()))
    full_name: str = Field(..., min_length=3, max_length=50, description="User's full name")
    username: str = Field(..., min_length=3, max_length=50, description="User's username")
    email: EmailStr = Field(..., description="User's email address")
    hashed_password: str = Field(..., description="Hashed password")
    is_active: bool = Field(default=True, description="If user account is active or not")
    role: str = Field(default="user", description="The role of the user (e.g., admin, user)")
    failed_login_attempts: int = Field(default=0, description="The number of failed login attempts")
    account_locked: bool = Field(default=False, description="Indicates if the account is locked due to failed logins")
    is_verified: bool = Field(default=True, description="Indicates if the user's email address has been verified")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="The account creation timestamp")
    updated_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

from pydantic import BaseModel, EmailStr
from typing import Optional

class CreateUserRequest(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    password: str
    full_name: str
    role: Optional[str] = "user" 
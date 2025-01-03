from backend.auth_service.users.models import UserModel
from fastapi.exceptions import HTTPException
from backend.auth_service.core.security import validate_and_hash_password, validate_email, validate_role
from datetime import datetime
from pymongo.database import Database

async def create_user_account(data: UserModel, db: Database):
    user = await db['users'].find_one({"email": data.email})
    if user:
        raise HTTPException(status_code=422, detail="Email is already registered with us.")

    new_user = {
        "username": data.username,
        "full_name": data.full_name,
        "email": validate_email(data.email),
        "hashed_password": validate_and_hash_password(data.password),
        "is_active": True,
        "role": validate_role(data.role),
        "failed_login_attempts": 0,
        "account_locked": False,
        "is_verified": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "last_login": None
    }
    await db['users'].insert_one(new_user)
    return new_user

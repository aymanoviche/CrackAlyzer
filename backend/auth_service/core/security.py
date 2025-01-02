from fastapi import HTTPException, Depends, status
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from starlette.authentication import AuthCredentials, UnauthenticatedUser
from passlib.context import CryptContext
from datetime import timedelta, datetime
from jose import jwt, JWTError
import os
import re
from bson import ObjectId
from backend.auth_service.core.config import get_settings
from backend.auth_service.core.database import get_db
from backend.auth_service.users.models import UserModel

settings = get_settings()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

BLOCKLIST_PATH = "backend/auth_service/core/disposable_email_blocklist.conf"

def is_email_allowed(email):
    try:
        # Validate email format
        if '@' not in email or email.startswith('@') or email.endswith('@'):
            raise HTTPException(status_code=400, detail="Invalid email format.")

        domain = email.split('@')[-1].strip()

        # # Check if blocklist file exists
        # if not os.path.exists(BLOCKLIST_PATH):
        #     print(f"Warning: Blocklist file '{BLOCKLIST_PATH}' not found.")
        #     return True  # If no blocklist file, allow the email by default.

        # Read blocklist file
        with open(BLOCKLIST_PATH, 'r') as file:
            blocked_domains = {line.strip() for line in file if line.strip()}

        # Check if the domain is in the blocklist
        if domain in blocked_domains:
            raise HTTPException(status_code=403,detail="Email is not allowed (Temporary emails are blacklisted).")

        return True
    except HTTPException as e:
        raise e

def validate_password(password: str):
    validation_results = {
        "length": len(password) >= 8,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "number": bool(re.search(r"\d", password)),
        "special_char": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)),
    }

    if not all(validation_results.values()):
        error_messages = []
        if not validation_results["length"]:
            error_messages.append("Password must be at least 8 characters long.")
        if not validation_results["uppercase"]:
            error_messages.append("Password must contain at least one uppercase letter.")
        if not validation_results["lowercase"]:
            error_messages.append("Password must contain at least one lowercase letter.")
        if not validation_results["number"]:
            error_messages.append("Password must contain at least one number.")
        if not validation_results["special_char"]:
            error_messages.append("Password must contain at least one special character.")
        
        raise HTTPException(status_code=422, detail="\n".join(error_messages))
    
    return validation_results

def hash_password(password: str) -> str:
    validate_password(password)
    return pwd_context.hash(password)


def validate_email(email):
    if not is_email_allowed(email):
        raise ValueError("Email is not allowed (Temporary emails are blacklisted).")
        raise HTTPException(status_code=422, detail="\n".join("Email is not allowed (Temporary emails are blacklisted)."))
    return email

def validate_and_hash_password(passowrd):
    validate_password(passowrd)
    return hash_password(passowrd)

def validate_role(role): 
    valid_roles = {"admin", "user"}
    if role not in valid_roles:
        raise ValueError(f"Invalid role: {role}. Valid roles are {valid_roles}.")
    return role

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) 


async def create_access_token(data,  expiry: timedelta):
    payload = data.copy()
    expire_in = datetime.utcnow() + expiry
    payload.update({"exp": expire_in})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)



async def create_refresh_token(data):
    return jwt.encode(data, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def get_token_payload(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None



class TokenData(BaseModel):
    username: str or None = None

class JWTAuth:
    async def authenticate(self, conn):
        guest = AuthCredentials(['unauthorized']), UnauthenticatedUser()

        if "authorization" not in conn.headers:
            return guest
        
        token = conn.headers.get('authorization').split(' ')[1]  # Token format: Bearer token_hash
        if not token:
            return guest
        
        try:
            # Await the async function
            user = await get_current_user(token=token)
        except HTTPException:
            return guest
        
        if not user:
            return guest
        
        return AuthCredentials(['authenticated']), user




# async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = get_token_payload(token=token)
#         if not payload or not isinstance(payload, dict):
#             raise credentials_exception

#         username: str = payload.get('username')
#         if username is None:
#             raise credentials_exception

#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception

#     # Fetch the user from the database
#     user = db['users'].find_one({"username": token_data.username})
#     if user is None:
#         raise credentials_exception

#     # Convert MongoDB dict to Pydantic model
#     user['_id'] = str(user['_id'])
#     return UserModel(**user)




async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Get database connection directly, no await needed
    db = next(get_db())
    
    payload = get_token_payload(token=token)
    if not payload or not isinstance(payload, dict):
        raise credentials_exception

    user_id = payload.get('id')
    if user_id is None:
        raise credentials_exception

    try:
        user_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid id",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = db['users'].find_one({"_id": user_id})
    if not user:
        raise credentials_exception
    if not user.get('is_active') or user.get('account_locked'):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive or locked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_model = UserModel(id=str(user["_id"]), **user)
    return user_model
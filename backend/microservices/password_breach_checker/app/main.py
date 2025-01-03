from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware
from backend.microservices.password_breach_checker.app.utils import check_password_breach
from backend.auth_service.users.models import UserModel
from backend.auth_service.core.security import oauth2_scheme, get_current_user
from pydantic import BaseModel
from backend.auth_service.core.database import BreachHistory
from datetime import datetime
from typing import List
from concurrent.futures import ThreadPoolExecutor
import asyncio

thread_pool = ThreadPoolExecutor(max_workers=5)

app = FastAPI(title="Password Breach Checker Microservice")

check_breach_router = APIRouter(
    prefix="/check-breach",
    tags=["check-breach"],
    responses={404: {"description": "Not found"}},
)

class PasswordRequest(BaseModel):
    password: str

# Add response model for history
class BreachHistoryResponse(BaseModel):
    timestamp: datetime
    password: str
    status: str
    message: str
    count: int

# Modify the check_breach endpoint to save history
@check_breach_router.post("/", status_code=status.HTTP_200_OK)
async def check_breach(request: PasswordRequest, token: str = Depends(oauth2_scheme), current_user: UserModel = Depends(get_current_user)):
    try:
        loop = asyncio.get_running_loop()
        
        # Check breach in thread pool
        count = await loop.run_in_executor(
            thread_pool,
            lambda: asyncio.run(check_password_breach(request.password))
        )
        
        result = {
            "password": request.password,
            "status": "Your Password Has Been Leaked",
            "message": f"This password has been seen {count:,} times :( Please do not use it!)",
            "count": count
        } if count > 0 else {
            "password": request.password,
            "status": "Your Password Is Safe :)",
            "message": "This password has not been leaked before. You're good to go!",
            "count": 0
        }
        
        # Save to DB using thread pool
        history_record = {
            "user_id": current_user.id,
            "password": request.password,
            "status": result["status"],
            "message": result["message"],
            "count": result["count"],
            "timestamp": datetime.utcnow()
        }
        
        await loop.run_in_executor(
            thread_pool,
            BreachHistory.insert_one,
            history_record
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@check_breach_router.get("/history", response_model=List[BreachHistoryResponse])
async def get_breach_history(token: str = Depends(oauth2_scheme), current_user: UserModel = Depends(get_current_user)):
    try:
        loop = asyncio.get_running_loop()
        
        # Get history using thread pool
        history = await loop.run_in_executor(
            thread_pool,
            lambda: list(BreachHistory.find(
                {"user_id": current_user.id},
                {"_id": 0, "user_id": 0}
            ).sort("timestamp", -1))
        )
        
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving breach history")


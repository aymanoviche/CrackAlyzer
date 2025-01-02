from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware
from backend.microservices.password_breach_checker.app.utils import check_password_breach
from backend.auth_service.users.models import UserModel
from backend.auth_service.core.security import oauth2_scheme, get_current_user
from pydantic import BaseModel
from backend.auth_service.core.database import BreachHistory
from datetime import datetime
from typing import List

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
        count = await check_password_breach(request.password)
        
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
        
        # Save the check result to database
        history_record = {
            "user_id": current_user.id,
            "password": request.password,
            "status": result["status"],
            "message": result["message"],
            "count": result["count"],
            "timestamp": datetime.utcnow()
        }
        BreachHistory.insert_one(history_record)
        
        return result
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

@check_breach_router.get("/history", response_model=List[BreachHistoryResponse])
async def get_breach_history(token: str = Depends(oauth2_scheme), current_user: UserModel = Depends(get_current_user)):
    try:
        # Get user's breach check history
        history = list(BreachHistory.find(
            {"user_id": current_user.id},
            {"_id": 0, "user_id": 0}  # Exclude only '_id' and 'user_id', but include 'password'
        ).sort("timestamp", -1))  # Sort by timestamp descending
        
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving breach history")
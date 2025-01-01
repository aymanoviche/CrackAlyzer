from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from fastapi.middleware.cors import CORSMiddleware
from backend.microservices.password_breach_checker.app.utils import check_password_breach
from backend.auth_service.users.models import UserModel
from backend.auth_service.core.security import oauth2_scheme, get_current_user
from pydantic import BaseModel

app = FastAPI(title="Password Breach Checker Microservice")

check_breach_router = APIRouter(
    prefix="/check-breach",
    tags=["check-breach"],
    responses={404: {"description": "Not found"}},
)

class PasswordRequest(BaseModel):
    password: str


@check_breach_router.post("/", status_code=status.HTTP_200_OK)
async def check_breach(request: PasswordRequest, token: str = Depends(oauth2_scheme), current_user: UserModel = Depends(get_current_user)):
    try:
        count = await check_password_breach(request.password)
        if count > 0:
            return {
                "status": "Your Password Has Been Leaked",
                "message": f"This password has been seen {count:,} times :( Please do not use it!)",
                "count": count
            }
        return {
            "status": "Your Password Is Safe :)",
            "message": "This password has not been leaked before. You're good to go!",
            "count": 0
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

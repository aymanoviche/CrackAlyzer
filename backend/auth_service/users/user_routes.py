from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from backend.auth_service.users.models import UserModel
from backend.auth_service.core.database import get_db
from backend.auth_service.users.schemas import CreateUserRequest
from backend.auth_service.users.user_services import create_user_account
from backend.auth_service.core.security import oauth2_scheme, get_current_user
from backend.auth_service.users.responses import UserResponse

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(oauth2_scheme)]
)



@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def create_user(user: CreateUserRequest, db = Depends(get_db)):
    await create_user_account(data=user, db=db)
    message = {"message": "User created successfully"}
    return JSONResponse(content=message, status_code=status.HTTP_201_CREATED)

@router.get("/me", response_model = UserResponse)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    return current_user


from fastapi import APIRouter,status,Depends,Header
from fastapi.security import OAuth2PasswordRequestForm
from backend.auth_service.core.database import get_db
from backend.auth_service.auth.auth_services import get_token, get_refresh_token


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/login",status_code=status.HTTP_200_OK)
async def login(data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    return await get_token(data = data, db = db)

@router.post("/refresh-token",status_code=status.HTTP_200_OK)
async def refresh_token(refresh_token: str = Header(), db = Depends(get_db)):
    return await get_refresh_token(token=refresh_token,db=db)
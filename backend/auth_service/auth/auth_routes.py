from fastapi import APIRouter, status, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from backend.auth_service.core.database import get_db
from backend.auth_service.auth.auth_services import get_token, get_refresh_token
from concurrent.futures import ThreadPoolExecutor
import asyncio

executor = ThreadPoolExecutor(max_workers=5) 

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(data: OAuth2PasswordRequestForm = Depends(), db = Depends(get_db)):
    # Run the token generation in a separate thread
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        executor,
        lambda: asyncio.run(get_token(data=data, db=db))
    )
    return result

@router.post("/refresh-token", status_code=status.HTTP_200_OK) 
async def refresh_token(refresh_token: str = Header(), db = Depends(get_db)):
    # Run the token refresh in a separate thread
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        executor,
        lambda: asyncio.run(get_refresh_token(token=refresh_token, db=db))
    )
    return result
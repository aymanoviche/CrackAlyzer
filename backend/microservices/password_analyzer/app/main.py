from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Depends, APIRouter, status
from datetime import datetime
from backend.auth_service.users.models import UserModel
from backend.microservices.password_analyzer.app.utils import analyze_password_strength, generate_strong_password
from backend.auth_service.core.security import oauth2_scheme, get_current_user
from backend.auth_service.core.database import PasswordAnalyzeHistory 
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import asyncio

app = FastAPI(title="Password Analyzer Microservice")

class PasswordAnalysisRequest(BaseModel):
    password: str

class PasswordAnalysisResponse(BaseModel):
    strength: str
    score: float
    details: dict
    suggested_password: str = None

analyzer_router = APIRouter(
    prefix="/analyze",
    tags=["analyze"],
    responses={404: {"description": "Not found"}},
)

process_pool = ProcessPoolExecutor(max_workers=5)
thread_pool = ThreadPoolExecutor(max_workers=5) 

@analyzer_router.post("/", status_code=status.HTTP_200_OK, response_model=PasswordAnalysisResponse)
async def analyze_password(request: PasswordAnalysisRequest, 
                         token: str = Depends(oauth2_scheme), 
                         current_user: UserModel = Depends(get_current_user)):
    try:
        loop = asyncio.get_running_loop()
        
        # Run password analysis in process pool
        analysis_result = await loop.run_in_executor(
            process_pool,
            analyze_password_strength,
            request.password
        )
        
        suggested_password = None
        if analysis_result['strength'] in ['Very Weak', 'Weak', 'Moderate', 'Strong']:
            suggested_password = await loop.run_in_executor(
                process_pool,
                generate_strong_password,
                request.password
            )
        
        # Prepare record
        analysis_record = {
            "user_id": current_user.id,
            "password": request.password,
            "strength": analysis_result['strength'],
            "score": analysis_result['score'],
            "details": analysis_result['details'],
            "suggested_password": suggested_password or "",
            "timestamp": datetime.utcnow()
        }
        
        # Save to DB using thread pool
        await loop.run_in_executor(
            thread_pool,
            PasswordAnalyzeHistory.insert_one,
            analysis_record
        )
        
        return PasswordAnalysisResponse(
            strength=analysis_result['strength'],
            score=analysis_result['score'],
            details=analysis_result['details'],
            suggested_password=suggested_password or ""
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@analyzer_router.get("/history", status_code=status.HTTP_200_OK)
async def get_password_analysis_history(token: str = Depends(oauth2_scheme), 
                                      current_user: UserModel = Depends(get_current_user)):
    try:
        loop = asyncio.get_running_loop()
        # Use thread pool for DB query
        history = await loop.run_in_executor(
            thread_pool,
            lambda: list(PasswordAnalyzeHistory.find({"user_id": current_user.id}, {"_id": 0}))
        )
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


app.include_router(analyzer_router)
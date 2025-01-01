from fastapi import FastAPI
from backend.auth_service.users.user_routes import router as guest_router, user_router
from backend.auth_service.auth.auth_routes import router as auth_router
from backend.microservices.password_analyzer.app.main import analyzer_router
from backend.microservices.password_breach_checker.app.main import check_breach_router
from backend.auth_service.core.security import JWTAuth
from starlette.middleware.authentication import AuthenticationMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(guest_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(analyzer_router)
app.include_router(check_breach_router)


# Add middleware
origins = [
    "http://localhost:5173",
    "http://crackalyzer.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthenticationMiddleware, backend=JWTAuth())


@app.get("/")
async def root():
    return {"message": "Hello World"}
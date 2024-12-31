from backend.auth_service.users.models import UserModel
from fastapi.exceptions import HTTPException
from backend.auth_service.core.security import verify_password
from backend.auth_service.core.config import get_settings
from datetime import timedelta
from backend.auth_service.core.security import create_access_token, create_refresh_token, get_token_payload
from backend.auth_service.auth.responses import TokenResponse
from bson import ObjectId

settings = get_settings()


async def get_token(data, db):
    user = db['users'].find_one({"username": data.username})
    
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Verify password
    if not verify_password(data.password, user['hashed_password']):
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Verify user access (active, verified, not locked)
    _verify_user_access(user=user)

    # Return tokens
    return await _get_user_token(user=user)


async def get_refresh_token(token, db):
    # Decode the refresh token payload
    payload = get_token_payload(token=token)
    user_id = payload.get('id', None)

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Convert user_id back to ObjectId for querying
    try:
        user_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Find the user by _id
    user = db['users'].find_one({"_id": user_id})
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Generate new tokens
    return await _get_user_token(user=user, refresh_token=token)


def _verify_user_access(user):
    # Check if the user is active
    if not user.get('is_active'):
        raise HTTPException(
            status_code=400,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Check if the user is verified
    if not user.get('is_verified'):
        raise HTTPException(
            status_code=400,
            detail="Email is not verified. A verification email has been sent to your email address.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Check if the account is locked
    if user.get('account_locked', False):
        raise HTTPException(
            status_code=400,
            detail="Account is locked",
            headers={"WWW-Authenticate": "Bearer"}
        )


async def _get_user_token(user, refresh_token=None):
    # Prepare the payload with the user's ID
    payload = {"id": str(user['_id'])}

    # Set token expiration times
    access_token_expiry = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN)
    refresh_token_expiry = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES_IN)

    # Create the access token
    access_token = await create_access_token(payload, access_token_expiry)

    # Create the refresh token if not provided
    if not refresh_token:
        refresh_token = await create_refresh_token(payload)

    # Return the token response
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expiry.seconds
    )

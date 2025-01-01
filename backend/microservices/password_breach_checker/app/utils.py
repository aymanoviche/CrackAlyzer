import hashlib
import httpx
from fastapi import HTTPException

async def check_password_breach(password: str):
    sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.pwnedpasswords.com/range/{prefix}",
                headers={"Add-Padding": "true"}
            )
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Error checking password breach")
    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="Failed to connect to the HIBP API")
    
    for line in response.text.splitlines():
        hash_suffix, count = line.split(':')
        if hash_suffix == suffix:
            return int(count)
    
    return 0

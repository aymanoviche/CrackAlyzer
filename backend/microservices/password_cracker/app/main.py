from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
import httpx
from bs4 import BeautifulSoup
from typing import List
import base64
from backend.microservices.password_cracker.app.hashidentifer import HashAnalyzer
import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from backend.auth_service.core.database import PasswordCrackerHistory
from backend.auth_service.core.security import oauth2_scheme, get_current_user
from backend.auth_service.users.models import UserModel
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Password Cracker Microservice")
process_pool = ProcessPoolExecutor(max_workers=5)
thread_pool = ThreadPoolExecutor(max_workers=5)

cracker_router = APIRouter(
    prefix="/password-cracker",
    tags=["password-cracker"],
    responses={404: {"description": "Not found"}},
)

class CrackerHistoryResponse(BaseModel):
    hash_string: str
    decrypted_string: str 
    hash_type: str
    timestamp: datetime

@cracker_router.get("/history", response_model=List[CrackerHistoryResponse])
async def get_cracker_history(token: str = Depends(oauth2_scheme), current_user: UserModel = Depends(get_current_user)):
    print(f"Token: {token}")
    print(f"Current user: {current_user}")

    try:
        loop = asyncio.get_running_loop()

        # Ensure the query for the user history is correct
        history = await loop.run_in_executor(
            thread_pool,
            lambda: list(PasswordCrackerHistory.find(
                {"user_id": current_user.id},  # Make sure the user_id matches
                {"_id": 0, "user_id": 0}  # Exclude _id and user_id fields from the result
            ).sort("timestamp", -1))  # Sort by timestamp descending
        )
        print(f"History retrieved: {history}")  # Add this debug line

        # Check if history was retrieved
        if not history:
            raise HTTPException(status_code=404, detail="No history found for this user.")

        return history

    except Exception as e:
        # If there's an error during fetching or processing
        raise HTTPException(status_code=500, detail=f"Error retrieving cracker history: {str(e)}")


@cracker_router.get("/{hash_string}")
async def decrypt_hash(hash_string: str, token: str = Depends(oauth2_scheme), current_user: UserModel = Depends(get_current_user)):
    hash_types = HashAnalyzer.identify_hash_type(hash_string)
    
    if not hash_types and not HashAnalyzer.is_possible_base64(hash_string):
        raise HTTPException(status_code=400, detail="Unsupported hash type or invalid hash string.")
    
    if 'md5' in hash_types:
        result = await decrypt_md5(hash_string)
        hash_type = 'md5'
    elif 'sha1' in hash_types:
        result = await decrypt_sha1(hash_string)
        hash_type = 'sha1'
    elif HashAnalyzer.is_possible_base64(hash_string):
        result = await decode_base64(hash_string)
        hash_type = 'base64'
    else:
        raise HTTPException(status_code=400, detail="Unsupported hash type or invalid hash string.")
    
    # Save the history in a direct way (no need for executor)
    history_record = {
        "user_id": current_user.id,
        "hash_string": hash_string,
        "decrypted_string": result["decrypted_string"],
        "hash_type": hash_type,
        "timestamp": datetime.utcnow()
    }

    # Ensure insert_one is the correct method to save data
    try:
        PasswordCrackerHistory.insert_one(history_record)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save history: {e}")
    
    return result

async def decrypt_md5(md5_hash: str):
    url = f"https://md5.gromweb.com/?md5={md5_hash}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from the website.")
    
    soup = BeautifulSoup(response.text, "html.parser")
    paragraph = soup.find("p", class_="word-break-all")
    
    if not paragraph:
        raise HTTPException(status_code=404, detail="Unable to find the decrypted string in the response.")
    
    string_link = paragraph.find("a", class_="String")
    if string_link:
        decrypted_string = string_link.text
        return {"md5_hash": md5_hash, "decrypted_string": decrypted_string}
    
    raise HTTPException(status_code=404, detail="Decrypted string not found.")

async def decrypt_sha1(sha1_hash: str):
    url = f"https://sha1.gromweb.com/?hash={sha1_hash}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from the website.")
    
    soup = BeautifulSoup(response.text, "html.parser")
    paragraph = soup.find("p", class_="word-break-all")
    
    if not paragraph:
        raise HTTPException(status_code=404, detail="Unable to find the decrypted string in the response.")
    
    string_link = paragraph.find("a", class_="String")
    if string_link:
        decrypted_string = string_link.text
        return {"sha1_hash": sha1_hash, "decrypted_string": decrypted_string}
    
    raise HTTPException(status_code=404, detail="Decrypted string not found.")

async def decode_base64(base64_input: str):
    try:
        decoded_bytes = base64.b64decode(base64_input, validate=True)
        decoded_string = decoded_bytes.decode("utf-8")
        return {"base64_input": base64_input, "decrypted_string": decoded_string}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Base64 input: {e}")




app.include_router(cracker_router)
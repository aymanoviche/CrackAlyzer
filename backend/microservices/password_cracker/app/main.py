from fastapi import FastAPI, HTTPException
import httpx
from bs4 import BeautifulSoup
import base64
from hashidentifer import HashAnalyzer

app = FastAPI()

@app.get("/decrypt-hash/{hash_string}")
async def decrypt_hash(hash_string: str):
    hash_types = HashAnalyzer.identify_hash_type(hash_string)
    
    if not hash_types and not HashAnalyzer.is_possible_base64(hash_string):
        raise HTTPException(status_code=400, detail="Unsupported hash type or invalid hash string.")
    
    if 'md5' in hash_types:
        return await decrypt_md5(hash_string)
    elif 'sha1' in hash_types:
        return await decrypt_sha1(hash_string)
    elif HashAnalyzer.is_possible_base64(hash_string):
        return await decode_base64(hash_string)
    else:
        raise HTTPException(status_code=400, detail="Unsupported hash type or invalid hash string.")

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
        return {"The type of your hash is : MD5": md5_hash, "Decrypted hash": decrypted_string}
    
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
        return {"The type of your hash is : SHA1": sha1_hash, "Decrypted hash": decrypted_string}
    
    raise HTTPException(status_code=404, detail="Decrypted string not found.")

async def decode_base64(base64_input: str):
    try:
        decoded_bytes = base64.b64decode(base64_input, validate=True)
        decoded_string = decoded_bytes.decode("utf-8")
        return {"The type of your hash is : BASE64": base64_input, "Decoded hash": decoded_string}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid Base64 input: {e}")
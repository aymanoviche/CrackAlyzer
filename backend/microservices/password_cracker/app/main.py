from fastapi import FastAPI, HTTPException
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

@app.get("/decrypt-md5/{md5_hash}")
async def decrypt_md5(md5_hash: str):
    url = f"https://md5.gromweb.com/?md5={md5_hash}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from the website.")
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    paragraph = soup.find("p", class_="word-break-all")
    
    if not paragraph:
        raise HTTPException(status_code=404, detail="Unable to find the decrypted string in the response.")
    
    # Extract the reversed string
    string_link = paragraph.find("a", class_="String")
    if string_link:
        decrypted_string = string_link.text
        return {"md5_hash": md5_hash, "decrypted_string": decrypted_string}
    
    raise HTTPException(status_code=404, detail="Decrypted string not found.")

@app.get("/decrypt-sha1/{sha1_hash}")
async def decrypt_sha1(sha1_hash: str):
    url = f"https://sha1.gromweb.com/?hash={sha1_hash}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch data from the website.")
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    paragraph = soup.find("p", class_="word-break-all")
    
    if not paragraph:
        raise HTTPException(status_code=404, detail="Unable to find the decrypted string in the response.")
    
    # Extract the reversed string
    string_link = paragraph.find("a", class_="String")
    if string_link:
        decrypted_string = string_link.text
        return {"sha1_hash": sha1_hash, "decrypted_string": decrypted_string}
    
    raise HTTPException(status_code=404, detail="Decrypted string not found.")
# ...existing code...

@app.get("/decrypt-sha224/{sha224_hash}")
async def decrypt_sha224(sha224_hash: str):
    url = f"https://md5hashing.net/hash/sha224/{sha224_hash}"
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
        return {"sha224_hash": sha224_hash, "decrypted_string": decrypted_string}
    raise HTTPException(status_code=404, detail="Decrypted string not found.")

@app.get("/decrypt-sha256/{sha256_hash}")
async def decrypt_sha256(sha256_hash: str):
    url = "https://10015.io/tools/sha256-encrypt-decrypt"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # Step 1: Send GET request to retrieve CSRF token
            get_response = await client.get(url)
            get_response.raise_for_status()
            
            # Parse HTML to find CSRF token
            soup = BeautifulSoup(get_response.text, "html.parser")
            csrf_input = soup.find("input", {"name": "__csrf"})
            if not csrf_input:
                raise HTTPException(status_code=400, detail="CSRF token not found.")
            csrf_token = csrf_input.get("value")
            
            # Step 2: Send POST request with hash and CSRF token
            data = {
                "hash": sha256_hash,
                "__csrf": csrf_token
            }
            post_response = await client.post(url, data=data, headers=headers)
            post_response.raise_for_status()
            
            # Parse POST response to get decrypted string
            soup = BeautifulSoup(post_response.text, "html.parser")
            result_div = soup.find("div", {"contenteditable": "false"})
            if not result_div:
                raise HTTPException(status_code=404, detail="Unable to find the decrypted string in the response.")
            decrypted_string = result_div.text.strip()
            return {"sha256_hash": sha256_hash, "decrypted_string": decrypted_string}
        
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch data from the website. HTTP error: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
@app.get("/decrypt-sha384/{sha384_hash}")
async def decrypt_sha384(sha384_hash: str):
    url = f"https://md5hashing.net/hash/sha384/{sha384_hash}"
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
        return {"sha384_hash": sha384_hash, "decrypted_string": decrypted_string}
    raise HTTPException(status_code=404, detail="Decrypted string not found.")

@app.get("/decrypt-sha512/{sha512_hash}")
async def decrypt_sha512(sha512_hash: str):
    url = f"https://md5hashing.net/hash/sha512/{sha512_hash}"
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
        return {"sha512_hash": sha512_hash, "decrypted_string": decrypted_string}
    raise HTTPException(status_code=404, detail="Decrypted string not found.")

@app.get("/decrypt-ripemd320/{ripemd320_hash}")
async def decrypt_ripemd320(ripemd320_hash: str):
    url = f"https://md5hashing.net/hash/ripemd320/{ripemd320_hash}"
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
        return {"ripemd320_hash": ripemd320_hash, "decrypted_string": decrypted_string}
    raise HTTPException(status_code=404, detail="Decrypted string not found.")
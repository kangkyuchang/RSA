from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import keyforge.generator as generator
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class PrimeNumber(BaseModel):
    p: int
    q: Optional[int] = None

class ValidExponent(BaseModel):
    e: int
    phi: int

class ManualKey(BaseModel):
    p: int
    q: int
    e: int

@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.get("/api/generate-key")
def generate_auto_key_api():
    result = generator.generate_auto_key()
    return {"publicKey": generator.key_to_base64(result[0]), 
            "privateKey": generator.key_to_base64(result[1]),
            "N": generator.key_to_base64(result[2])}

@app.post("/api/generate-key")
def generate_manual_key_api(data: ManualKey):
    result = generator.generate_manual_key(data.p, data.q, data.e)
    return {"status": result[0],
            "publicKey": generator.key_to_base64(result[1]), 
            "privateKey": generator.key_to_base64(result[2]),
            "N": generator.key_to_base64(result[3])}

@app.post("/api/check-prime")
def check_prime_api(number: PrimeNumber):
    is_prime = generator.is_prime(number.p)
    return { "isPrime": is_prime }

@app.post("/api/get-phi")
def get_phi_api(numbers: PrimeNumber):
    if numbers.p != numbers.q:
        is_vaild = generator.is_prime(numbers.p) & generator.is_prime(numbers.q)
    else:  
        is_vaild = False
    PHI = generator.phi(numbers.p, numbers.q) if is_vaild else 0 
    return {"isValid": is_vaild,
            "phi": PHI}

@app.post("/api/check-exponent")
def check_e_api(number: ValidExponent):
    if number.phi > 65537:
        is_valid = False
    else:
        validNumbers = generator.create_exponent(number.phi)
        is_valid = number.e in validNumbers

    return { "isValid": is_valid }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
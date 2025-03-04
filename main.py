
# #uvicorn main:app --reload

from fastapi import FastAPI, Depends, HTTPException, Header
import ollama
import os
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize API credits
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY is missing in environment variables")

API_KEY_CREDITS = {API_KEY: 5}

# Initialize FastAPI app
app = FastAPI()

def verify_api_key(x_api_key: str = Header(None)):
    if not x_api_key or x_api_key not in API_KEY_CREDITS:
        raise HTTPException(status_code=401, detail="Invalid key or no credits")
    
    if API_KEY_CREDITS[x_api_key] <= 0:
        raise HTTPException(status_code=403, detail="No remaining credits")
    
    return x_api_key

@app.post("/generate")
def generate(prompt: str, x_api_key: str = Depends(verify_api_key)):
    # Deduct credit
    API_KEY_CREDITS[x_api_key] -= 1
    
    try:
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": prompt}])
        return {"response": response['message']['content']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8085)

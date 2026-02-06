import os
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

load_dotenv()

security = HTTPBearer()

def verify_api_key(auth: HTTPAuthorizationCredentials = Security(security)):
    expected_key = os.getenv("API_KEY")
    if not expected_key:
        # In a real app, you might want to log this as a misconfiguration
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API Key not configured on server"
        )
    
    if auth.credentials != expected_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth.credentials

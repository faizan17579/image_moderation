from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
DB_NAME = "image_moderation"

security = HTTPBearer()

async def get_db():
    client = AsyncIOMotorClient(MONGO_URI)
    try:
        db = client[DB_NAME]
        yield db
    finally:
        client.close()

async def get_current_token(credentials: HTTPAuthorizationCredentials = Depends(security), db=Depends(get_db)):
    token = credentials.credentials
    token_doc = await db.tokens.find_one({"token": token})
    if not token_doc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_doc

async def get_admin_token(token_doc: dict = Depends(get_current_token)):
    if not token_doc.get("isAdmin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return token_doc
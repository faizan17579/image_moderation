from fastapi import APIRouter, Depends, HTTPException, status
from ..dependencies import get_db, get_admin_token
from ..models import Token
from datetime import datetime
import uuid

router = APIRouter()

@router.post("/tokens")
async def create_token(isAdmin: bool = False, db=Depends(get_db), _=Depends(get_admin_token)):
    token = str(uuid.uuid4())
    token_doc = Token(token=token, isAdmin=isAdmin, createdAt=datetime.utcnow())
    await db.tokens.insert_one(token_doc.dict())
    await db.usages.insert_one({"token": token, "endpoint": "/auth/tokens", "timestamp": datetime.utcnow()})
    return {"token": token}

@router.get("/tokens")
async def list_tokens(db=Depends(get_db), _=Depends(get_admin_token)):
    tokens = await db.tokens.find().to_list(length=None)
    await db.usages.insert_one({"token": _["token"], "endpoint": "/auth/tokens", "timestamp": datetime.utcnow()})
    return tokens

@router.delete("/tokens/{token}")
async def delete_token(token: str, db=Depends(get_db), _=Depends(get_admin_token)):
    result = await db.tokens.delete_one({"token": token})
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Token not found")
    await db.usages.insert_one({"token": _["token"], "endpoint": f"/auth/tokens/{token}", "timestamp": datetime.utcnow()})
    return {"message": "Token deleted"}
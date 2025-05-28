from fastapi import APIRouter, Depends, UploadFile, File
from ..dependencies import get_db, get_current_token
from ..models import ModerationResponse, ModerationResult
from datetime import datetime

router = APIRouter()

def analyze_image(image: UploadFile) -> ModerationResult:
    # Placeholder: Replace with real image moderation logic (e.g., NSFW.js, AWS Rekognition)
    # For demo, return mock results
    return ModerationResult(
        is_safe=True,
        categories={"violence": 0.1, "nudity": 0.05, "hate_symbols": 0.01}
    )

@router.post("")
async def moderate_image(file: UploadFile = File(...), db=Depends(get_db), token_doc=Depends(get_current_token)):
    result = analyze_image(file)
    await db.usages.insert_one({"token": token_doc["token"], "endpoint": "/moderate", "timestamp": datetime.utcnow()})
    return ModerationResponse(result=result)
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict

class Token(BaseModel):
    token: str
    isAdmin: bool
    createdAt: datetime

class Usage(BaseModel):
    token: str
    endpoint: str
    timestamp: datetime

class ModerationResult(BaseModel):
    is_safe: bool
    categories: Dict[str, float]  # e.g., {"violence": 0.9, "nudity": 0.1}

class ModerationResponse(BaseModel):
    result: ModerationResult
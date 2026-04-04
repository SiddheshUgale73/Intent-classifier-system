from pydantic import BaseModel
from typing import Optional, Dict, Any

class IntentRequest(BaseModel):
    text: str

class IntentResponse(BaseModel):
    intent: str
    confidence: float
    text: str
    entities: Optional[Dict[str, Any]] = None

class HealthCheck(BaseModel):
    status: str

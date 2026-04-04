from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class IntentRequest(BaseModel):
    text: str

class IntentResult(BaseModel):
    """Reflects a single intent within the multi-intent result."""
    intent: str
    confidence: float
    entities: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    common_approaches: Optional[List[str]] = None
    suggested_action: Optional[str] = None

class IntentResponse(BaseModel):
    """The main response object for multi-intent detection."""
    status: str
    input: str
    intents: List[IntentResult]
    timestamp: str

class HealthCheck(BaseModel):
    status: str

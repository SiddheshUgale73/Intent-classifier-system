from fastapi import APIRouter, HTTPException
import os
import sys

# Add parent directory to sys.path for local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.schemas import IntentRequest, IntentResponse, HealthCheck
from model.predict import load_model
from utils.multi_intent import detect_multi_intent

router = APIRouter()

@router.get("/health", response_model=HealthCheck)
def health_check():
    """
    Checks if the API is running and the models are loaded.
    """
    try:
        load_model()
        return HealthCheck(status="healthy")
    except Exception:
        return HealthCheck(status="unhealthy - model or encoder missing")

@router.post("/predict", response_model=IntentResponse)
def predict(request: IntentRequest):
    """
    Predicts multiple intents using the multi_intent utility.
    """
    try:
        # Use the multi-intent logic to handle complex queries
        result = detect_multi_intent(request.text)
        
        # The result structure matches the new IntentResponse schema
        return IntentResponse(
            status=result["status"],
            input=result["input"],
            intents=result["intents"],
            timestamp=result["timestamp"]
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        print(f"Multi-intent prediction error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during prediction.")

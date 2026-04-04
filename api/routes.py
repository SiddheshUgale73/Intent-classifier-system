from fastapi import APIRouter, HTTPException
import os
import sys

# Add parent directory to sys.path for local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.schemas import IntentRequest, IntentResponse, HealthCheck
from model.predict import predict_intent, load_model

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
    Predicts the intent using the model/predict module.
    """
    try:
        result = predict_intent(request.text)
        return IntentResponse(
            intent=result["intent"],
            confidence=result["confidence"],
            text=request.text,
            entities=result.get("entities")
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        print(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during prediction.")

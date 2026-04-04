from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import os
import sys

# Add parent directory to sys.path for local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.predict import predict_intent, load_model

# Initialize the FastAPI app
app = FastAPI(
    title="Intent Classification & Entity Extraction API",
    description="Production-ready API for banking assistant intents.",
    version="1.0.0"
)

# Schemas
class IntentRequest(BaseModel):
    text: str

class IntentResponse(BaseModel):
    intent: str
    confidence: float
    text: str
    entities: Optional[Dict[str, Any]] = None

class HealthCheck(BaseModel):
    status: str
    model_loaded: bool

# Startup event to ensure models are ready
@app.on_event("startup")
async def startup_event():
    try:
        load_model()
        print("Models loaded successfully at startup.")
    except Exception as e:
        print(f"Warning: Model loading failed: {e}")

@app.get("/health", response_model=HealthCheck)
def health_check():
    """
    Checks if the API is running and the models are available.
    """
    try:
        load_model()
        return HealthCheck(status="healthy", model_loaded=True)
    except Exception:
        return HealthCheck(status="unhealthy", model_loaded=False)

@app.post("/predict", response_model=IntentResponse)
def predict(request: IntentRequest):
    """
    Predicts intent and extracts entities for a given text.
    Steps:
    1. Preprocessing (integrated in predict_intent)
    2. Embedding Prediction (integrated in predict_intent)
    3. Entity Extraction (integrated in predict_intent)
    """
    if not request.text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    try:
        # Integrated model and entity extraction call
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
        raise HTTPException(status_code=500, detail="Internal server error during processing.")

if __name__ == "__main__":
    import uvicorn
    # Use 'app:app' for reload/production if running directly
    uvicorn.run(app, host="0.0.0.0", port=8000)

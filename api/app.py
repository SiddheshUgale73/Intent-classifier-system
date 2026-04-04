from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "ui", "static")

# Mount Static Files
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

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

@app.get("/")
async def read_index():
    """Serves the main HTML UI."""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/style.css")
async def read_css():
    """Serves the CSS file."""
    return FileResponse(os.path.join(STATIC_DIR, "style.css"))

@app.get("/script.js")
async def read_js():
    """Serves the JS file."""
    return FileResponse(os.path.join(STATIC_DIR, "script.js"))

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
        raise HTTPException(status_code=500, detail="Internal server error during prediction.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

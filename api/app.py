from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
import sys

# Add parent directory to sys.path for local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.predict import load_model
from api.routes import router

# Initialize the FastAPI app
app = FastAPI(
    title="Banking Intent Assistant API",
    description="Multi-intent detection and entity extraction engine.",
    version="1.2.0"
)

# Startup event to ensure models are ready
@app.on_event("startup")
async def startup_event():
    try:
        load_model()
        print("Models loaded successfully at startup.")
    except Exception as e:
        print(f"Warning: Model loading failed: {e}")

# Include the main prediction and health routes
app.include_router(router)

# Paths for static UI (Legacy Fallback)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "ui", "static")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

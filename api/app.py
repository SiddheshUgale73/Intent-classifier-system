from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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
    version="1.5.0"
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

# Paths for static UI
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "ui", "static")

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

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

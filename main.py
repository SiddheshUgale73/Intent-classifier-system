import subprocess
import time
import os

def run_app():
    """
    Launches the FastAPI backend which serves the HTML UI.
    """
    print("Starting Intent Classification System...")
    
    # Start FastAPI
    print("Launching API & Web UI at http://localhost:8000...")
    try:
        # Launching synchronously since it's the only process now
        import uvicorn
        uvicorn.run("api.app:app", host="127.0.0.1", port=8000, reload=False)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        print("Done!")

if __name__ == "__main__":
    run_app()

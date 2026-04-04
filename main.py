import subprocess
import time
import os

def run_app():
    """
    Launches the FastAPI backend and Streamlit UI.
    """
    print("Starting Intent Classification System...")
    
    # 1. Start FastAPI in the background
    print("Launching API...")
    # Using python -m uvicorn or similar
    api_proc = subprocess.Popen(["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"])
    
    # Wait for API to start
    time.sleep(2)
    
    # 2. Start Streamlit
    print("Launching UI...")
    try:
        subprocess.run(["streamlit", "run", "ui/app.py"])
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        api_proc.terminate()
        print("Done!")

if __name__ == "__main__":
    run_app()

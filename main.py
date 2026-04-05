import subprocess
import os
import sys

def check_dependencies():
    """Checks for required dependencies and provides advice if missing."""
    required = ["uvicorn", "fastapi"]
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"Missing required dependencies: {', '.join(missing)}")
        print("\nPlease run the following command to install them:")
        print("    pip install -r requirements.txt")
        print("\nIf you are using a virtual environment, make sure it's activated:")
        print("    .\\.venv\\Scripts\\activate")
        sys.exit(1)

def run_app():
    """Launches the FastAPI backend."""
    check_dependencies()
    
    print("Starting Intent Classification System...")
    print("Launching API & Web UI at http://localhost:8000...")
    
    try:
        import uvicorn
        uvicorn.run("api.app:app", host="127.0.0.1", port=8000, reload=False)
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Failed to start server: {e}")
    finally:
        print("Done!")

if __name__ == "__main__":
    run_app()

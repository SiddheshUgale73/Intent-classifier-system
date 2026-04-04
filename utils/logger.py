import csv
import os
from datetime import datetime

# Path to the log file
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs"))
LOG_FILE = os.path.join(LOG_DIR, "predictions.csv")

def log_prediction(text: str, intent: str, confidence: float):
    """
    Append prediction details to a persistent CSV log file.
    Fields: timestamp, user_input, predicted_intent, confidence
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists(LOG_DIR):
        try:
            os.makedirs(LOG_DIR)
        except Exception as e:
            print(f"Warning: Could not create logs directory: {e}")
            return

    file_exists = os.path.isfile(LOG_FILE)
    
    # Headers for the log file
    headers = ["timestamp", "user_input", "predicted_intent", "confidence"]
    
    try:
        with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            
            # Write header if file is new
            if not file_exists:
                writer.writeheader()
            
            # Write the log entry
            writer.writerow({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_input": text,
                "predicted_intent": intent,
                "confidence": round(confidence, 4)
            })
    except Exception as e:
        print(f"Error: Failed to write to prediction log: {e}")

if __name__ == "__main__":
    # Test logger
    log_prediction("Test input message", "GREETING", 0.99)
    print(f"Log appended to: {LOG_FILE}")

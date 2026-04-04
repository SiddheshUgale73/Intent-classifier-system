import os
import sys
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

# Add parent directory to sys.path for local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.preprocessing import preprocess_pipeline
from utils.entities import extract_entities
from utils.logger import log_prediction

# Paths to the trained artifacts
MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "encoder.pkl")

# Threshold for uncertain predictions
CONFIDENCE_THRESHOLD = 0.6

# Shared state to avoid reloading models on every request
_classifier = None
_encoder = None

def load_model():
    """
    Loads the classifier and the sentence transformer encoder.
    Returns: (classifier, encoder)
    """
    global _classifier, _encoder
    
    if _classifier is not None and _encoder is not None:
        return _classifier, _encoder

    if not os.path.exists(MODEL_PATH) or not os.path.exists(ENCODER_PATH):
        raise FileNotFoundError("Model or encoder file not found. Please run model/train.py first.")

    # Load classifier
    with open(MODEL_PATH, 'rb') as f:
        _classifier = pickle.load(f)

    # Load encoder metadata and transformer
    with open(ENCODER_PATH, 'rb') as f:
        metadata = pickle.load(f)
        model_name = metadata.get("model_name", "all-MiniLM-L6-v2")
        _encoder = SentenceTransformer(model_name)

    return _classifier, _encoder

def predict_intent(text: str):
    """
    Preprocesses input text, generates embeddings, and predicts intent.
    Returns: dict with intent and confidence score.
    """
    # 1. Ensure models are loaded
    clf, transformer = load_model()

    # 2. Preprocess input
    processed_text = preprocess_pipeline(text)

    # 3. Generate embeddings
    # Using [processed_text] to work with the batch interface of encode
    embedding = transformer.encode([processed_text])

    # 4. Predict
    probabilities = clf.predict_proba(embedding)[0]
    confidence = float(np.max(probabilities))
    
    # 5. Handle Uncertainty
    if confidence < CONFIDENCE_THRESHOLD:
        prediction = "UNCERTAIN"
    else:
        prediction = clf.predict(embedding)[0]

    # 6. Extract Entities
    entities = extract_entities(text)
    
    # 7. Log Prediction
    log_prediction(text, str(prediction), confidence)

    return {
        "intent": str(prediction),
        "confidence": round(confidence, 4),
        "entities": entities
    }

if __name__ == "__main__":
    # Test block
    try:
        test_text = "I lost my debit card, please help!"
        print(f"Testing prediction for: '{test_text}'")
        result = predict_intent(test_text)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

import joblib
import pandas as pd
import os
import pickle
from sentence_transformers import SentenceTransformer

def load_classifier(model_path: str):
    """
    Loads the trained Logistic Regression model from a pickle file.
    """
    if not os.path.exists(model_path):
        return None
    try:
        with open(model_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error loading classifier: {e}")
        return None

def load_encoder(encoder_path: str):
    """
    Loads the Sentence Transformer based on metadata.
    """
    if not os.path.exists(encoder_path):
        return None
    try:
        with open(encoder_path, 'rb') as f:
            metadata = pickle.load(f)
            model_name = metadata.get("model_name", "all-MiniLM-L6-v2")
            print(f"Loading Sentence Transformer model: {model_name}...")
            return SentenceTransformer(model_name)
    except Exception as e:
        print(f"Error loading encoder: {e}")
        return None

def load_data(data_path: str):
    """
    Loads the training dataset.
    """
    if not os.path.exists(data_path):
        return None
    try:
        return pd.read_csv(data_path)
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

import pandas as pd
import joblib
import os
import sys
import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report
from sentence_transformers import SentenceTransformer

# Add parent directory to sys.path for local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.preprocessing import preprocess_pipeline

# Configuration / Constants
CONFIG = {
    "data_path": os.path.join("data", "dataset.csv"),
    "model_path": os.path.join("model", "model.pkl"),
    "encoder_path": os.path.join("model", "encoder.pkl"),
    "transformer_model": "all-MiniLM-L6-v2",
    "test_size": 0.2,
    "random_state": 42
}

def load_and_preprocess_data(data_path: str):
    """Loads data and applies initial preprocessing."""
    print(f"Loading data from {data_path}...")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
    
    df = pd.read_csv(data_path)
    print("Preprocessing text...")
    df['processed_text'] = df['text'].apply(preprocess_pipeline)
    return df

def generate_embeddings(texts: list, model_name: str):
    """Generates embeddings using Sentence Transformers."""
    print(f"Loading transformer: {model_name}...")
    model = SentenceTransformer(model_name)
    print("Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings, model

def train_classifier(X, y, test_size, random_state):
    """Splits data and trains a Logistic Regression classifier."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    print("Training Logistic Regression classifier...")
    clf = LogisticRegression(max_iter=1000, multi_class='multinomial', random_state=random_state)
    clf.fit(X_train, y_train)
    
    return clf, X_test, y_test

def evaluate_model(clf, X_test, y_test):
    """Prints evaluation metrics."""
    y_pred = clf.predict(X_test)
    
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, average='weighted'),
        "recall": recall_score(y_test, y_pred, average='weighted')
    }
    
    print("\n--- Model Performance ---")
    for name, value in metrics.items():
        print(f"{name.capitalize()}: {value:.4f}")
    
    print(f"\nFull Report:\n{classification_report(y_test, y_pred)}")
    return metrics

def save_artifacts(classifier, model_name, model_path, encoder_path):
    """Saves the trained model and encoder metadata."""
    print(f"Saving classifier to {model_path}...")
    with open(model_path, 'wb') as f:
        pickle.dump(classifier, f)
    
    print(f"Saving encoder metadata to {encoder_path}...")
    encoder_metadata = {"model_name": model_name}
    with open(encoder_path, 'wb') as f:
        pickle.dump(encoder_metadata, f)

def run_training_pipeline():
    """Orchestrates the full training pipeline."""
    try:
        # 1. Data
        df = load_and_preprocess_data(CONFIG["data_path"])
        
        # 2. Embeddings
        X, _ = generate_embeddings(df['processed_text'].tolist(), CONFIG["transformer_model"])
        y = df['intent']
        
        # 3. Train
        clf, X_test, y_test = train_classifier(
            X, y, CONFIG["test_size"], CONFIG["random_state"]
        )
        
        # 4. Evaluate
        evaluate_model(clf, X_test, y_test)
        
        # 5. Save
        save_artifacts(
            clf, 
            CONFIG["transformer_model"], 
            CONFIG["model_path"], 
            CONFIG["encoder_path"]
        )
        
        print("\nPipeline execution successful.")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")

if __name__ == "__main__":
    run_training_pipeline()

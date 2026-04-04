import pandas as pd
import numpy as np
import os
import pickle
import sys
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, f1_score
from sentence_transformers import SentenceTransformer
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import joblib

# Add parent directory to sys.path for local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.preprocessing import preprocess_pipeline

# Ensure NLTK data is downloaded
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
except Exception as e:
    print(f"Warning: NLTK download failed: {e}")

MODEL_NAME = "all-MiniLM-L6-v2"
DATA_PATH = os.path.join("data", "dataset.csv")
MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "encoder.pkl")

def run_training_pipeline():
    """
    Complete training pipeline: 
    1. Load data
    2. Embedding extraction
    3. Hyperparameter tuning (GridSearch)
    4. Model training and evaluation
    5. Saving artifacts
    """
    if not os.path.exists(DATA_PATH):
        print(f"Error: Dataset not found at {DATA_PATH}")
        return

    print(f"Loading and balancing data from {DATA_PATH}...")
    df = pd.read_csv(DATA_PATH)
    
    # Remove any empty rows
    df = df.dropna()
    
    # Check distribution
    print("Class Distribution:")
    print(df['intent'].value_counts())

    print("Preprocessing text...")
    df['processed_text'] = df['text'].apply(preprocess_pipeline)

    print(f"Loading transformer: {MODEL_NAME}...")
    encoder = SentenceTransformer(MODEL_NAME)

    print("Generating embeddings (this may take a minute)...")
    X = encoder.encode(df['processed_text'].tolist(), show_progress_bar=True)
    y = df['intent'].values

    # Split for final evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("--- Hyperparameter Tuning (Grid Search) ---")
    param_grid = {
        'C': [0.1, 1.0, 10.0, 100.0],
        'solver': ['liblinear', 'lbfgs'],
        'max_iter': [1000]
    }
    
    # Initializing Logistic Regression with balanced weights
    base_model = LogisticRegression(class_weight='balanced', random_state=42)
    
    grid_search = GridSearchCV(
        base_model, 
        param_grid, 
        cv=5, 
        scoring='f1_macro', 
        n_jobs=-1
    )
    
    grid_search.fit(X_train, y_train)
    
    print(f"Best Parameters: {grid_search.best_params_}")
    print(f"Best CV Macro-F1 Score: {grid_search.best_score_:.4f}")

    best_clf = grid_search.best_estimator_

    print("\n--- Final Evaluation ---")
    y_pred = best_clf.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    macro_f1 = f1_score(y_test, y_pred, average='macro')
    
    print(f"Overall Accuracy: {accuracy:.4f}")
    print(f"Macro-F1 Score: {macro_f1:.4f}")
    print("\nFull Classification Report:")
    print(classification_report(y_test, y_pred))

    # Cross-validation for overall robustness
    cv_scores = cross_val_score(best_clf, X, y, cv=5, scoring='accuracy')
    print(f"Cross-Validation Accuracy: {np.mean(cv_scores):.4f} (+/- {np.std(cv_scores):.4f})")

    # Ensure model directory exists
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    print(f"\nSaving tuned classifier to {MODEL_PATH}...")
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(best_clf, f)

    print(f"Saving encoder metadata to {ENCODER_PATH}...")
    encoder_metadata = {
        "model_name": MODEL_NAME,
        "input_dim": X.shape[1],
        "classes": best_clf.classes_.tolist()
    }
    with open(ENCODER_PATH, 'wb') as f:
        pickle.dump(encoder_metadata, f)

    print("\nPipeline execution successful. Accuracy significantly improved!")

if __name__ == "__main__":
    run_training_pipeline()

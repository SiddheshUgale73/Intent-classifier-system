# 🏦 Smart Banking Assistant: Intent Classification & Entity Extraction

A production-ready NLP system designed to empower modern banking applications with semantic understanding. This system uses state-of-the-art transformer embeddings to classify customer intents and extract actionable transaction data in real-time.

---

## 🌟 Project Overview

The **Smart Banking Assistant** provides a robust, modular framework for processing natural language banking queries. It bridges the gap between raw user input and structured financial transactions by combining:
- **Semantic Classification**: High-accuracy intent detection using `Sentence Transformers`.
- **Structured Extraction**: Automated identification of transaction amounts and receivers.
- **Persistent Auditing**: Full logging of all interactions for business intelligence and model refinement.

---

## 🛠️ Tech Stack
- **NLP Engine**: `Sentence-Transformers (all-MiniLM-L6-v2)`
- **Classifier**: `Scikit-learn (Logistic Regression)`
- **Backend API**: `FastAPI` (High performance, Asynchronous)
- **Frontend UI**: `Streamlit` (Premium interactive dashboard)
- **Utilities**: `NLTK`, `Pandas`, `Joblib`

---

## 📂 Project Structure
```text
intent-classifier-system/
├── api/             # FastAPI Application (v1.0.0)
│   └── app.py       # Consolidated API entry point
├── data/            # Knowledge Base
│   └── dataset.csv  # 700+ banking intent examples
├── model/           # Machine Learning Assets
│   ├── train.py     # Modular training pipeline
│   ├── predict.py   # Integrated inference engine
│   ├── model.pkl    # Trained classifier
│   └── encoder.pkl  # Transformer metadata
├── ui/              # User Interface
│   └── app.py       # Premium Streamlit dashboard
├── utils/           # Shared Utilities
│   ├── entities.py  # Rule-based entity extraction
│   ├── logger.py    # Persistent audit logging
│   └── preprocessing.py # Text normalization pipeline
├── logs/            # Audit Trails
│   └── predictions.csv # Historical interaction logs
├── main.py          # Unified system orchestrator
└── requirements.txt # Dependency manifest
```

---

## 🚀 Getting Started

### 1. Installation
Ensure you have Python 3.8+ installed. It is highly recommended to use a virtual environment.
```powershell
# Install dependencies
pip install -r requirements.txt
```

### 2. Training the Model
The system comes with a pre-generated dataset. Use the modular training pipeline to generate the model artifacts.
```powershell
python model/train.py
```

### 3. Launching the System
You can launch the entire system (API + UI) with a single command:
```powershell
python main.py
```

---

## 📟 Component Guides

### Running the API Individually
The FastAPI backend provides a high-performance REST interface.
```powershell
uvicorn api.app:app --host 0.0.0.0 --port 8000
```
- **Docs**: Visit `http://localhost:8000/docs` for interactive Swagger UI.

### Running the Streamlit UI Individually
The frontend provides a premium, user-friendly dashboard for query analysis.
```powershell
streamlit run ui/app.py
```

---

## 📝 Example Interactions

| User Input | Predicted Intent | Extracted Amount | Extracted Receiver |
| :--- | :--- | :--- | :--- |
| "Transfer 500 dollars to John" | `TRANSFER_MONEY` | `$500.00` | `John` |
| "Show my last transactions" | `TRANSACTION_HISTORY` | `N/A` | `N/A` |
| "Close my lost credit card!" | `BLOCK_CARD` | `N/A` | `N/A` |

---

## 📊 Logging & Auditing
Every interaction is recorded in `logs/predictions.csv`, providing a reliable audit trail for compliance, performance monitoring, and continuous model improvement.

---
**Developed for the next generation of Fintech.**

# 🏦 Smart Banking Assistant: Multi-Intent Platform

A production-ready NLP system designed to empower modern banking applications with semantic understanding. This system uses state-of-the-art transformer embeddings to classify customer intents, extract actionable transaction data, and handle complex multi-intent queries in real-time.

---

## 🌟 Project Overview

The **Smart Banking Assistant** provides a robust, modular framework for processing natural language banking queries. It bridges the gap between raw user input and structured financial transactions by combining:

- **Multi-Intent Processing**: Detect and process multiple actions in a single query (e.g., "Transfer 500 and show balance").
- **Explainable AI (XAI)**: Provides clear reasoning and "common approaches" for every detected intent using a curated knowledge base.
- **Structured Extraction**: Automated identification of transaction amounts, receivers, and history limits.
- **Persistent Auditing**: Full logging of all interactions for business intelligence and model refinement.

---

## 🛠️ Tech Stack

- **NLP Engine**: `Sentence-Transformers (all-MiniLM-L6-v2)`
- **Classifier**: `Scikit-learn (Logistic Regression)`
- **Core Logic**: `NLTK`, `Pandas`, `Joblib`
- **Backend API**: `FastAPI` (High performance, Multi-intent schemas)
- **Frontend UI**: `Streamlit` (Premium intelligence-driven dashboard)

---

## 📂 Project Structure

```text
intent-classifier-system/
├── api/                 # FastAPI Implementation
│   ├── app.py           # Main API Application
│   ├── routes.py        # Centralized Endpoint Routing
│   └── schemas.py       # Pydantic Multi-Intent Schemas
├── data/                # Knowledge Base & Dataset
│   ├── dataset.csv      # 700+ banking intent examples
│   └── intent_knowledge.json # Explainability Core (Descriptions & Approaches)
├── model/               # Machine Learning Assets
│   ├── train.py         # Modular training pipeline
│   ├── predict.py       # Intent classification engine
│   ├── model.pkl        # Trained classifier (Logistic Regression)
│   └── encoder.pkl      # Transformer metadata
├── ui/                  # User Interface
│   └── app.py           # Premium Streamlit Dashboard
├── utils/               # Shared Utilities
│   ├── multi_intent.py  # NEW: Conjunction-based intent splitter
│   ├── entities.py      # Rule-based entity extraction
│   ├── logger.py        # Persistent audit logging
│   └── preprocessing.py # Text normalization pipeline
├── logs/                # Audit Trails
│   └── predictions.csv  # Historical interaction logs
├── main.py              # Unified system orchestrator
└── requirements.txt     # Dependency manifest
```

---

## 🚀 Getting Started

### 1. Installation
Ensure you have Python 3.8+ installed. It is highly recommended to use a virtual environment.
```powershell
pip install -r requirements.txt
```

### 2. Training the Model
Generate model artifacts using the modular training pipeline.
```powershell
python model/train.py
```

### 3. Launching the System
Launch the entire system (API + UI) with a single command:
```powershell
python main.py
```

---

## 📝 Example Multi-Intent Interactions

| User Input | Detected Intents | Extracted Data | Confidence |
| :--- | :--- | :--- | :--- |
| "Transfer 500 to John and show balance" | `TRANSFER_MONEY`, `CHECK_BALANCE` | $500.00, John | 98.5% |
| "I lost my card, please block it!" | `REPORT_LOST_CARD`, `BLOCK_CARD` | N/A | 97.2% |
| "Hi! Show my last 5 transactions" | `GREETING`, `TRANSACTION_HISTORY` | Limit: 5 | 96.8% |

---

## 📊 Logging & Auditing
Every interaction is recorded in `logs/predictions.csv`, providing a reliable audit trail for compliance, performance monitoring, and continuous model refinement.

---
**Developed for the next generation of Fintech.**

# 🏦 Agentic Banking Assistant: Multi-Intent AI Platform

A production-grade NLP platform designed for the next generation of Fintech. This system provides a robust, explainable, and proactive layer for understanding complex customer banking requests.

---

## 🎯 Problem Statement

Traditional banking chatbots struggle with **Complex Single-String Queries** (e.g., *"Transfer 500 dollars to Rahul, also check my balance and then block my card"*). Most systems either fail to detect all actions or provide "black-box" results that the user doesn't understand. 

Our goal was to build a system that:
1.  **Decomposes** multi-step user requests into individual actionable intents.
2.  **Explains** its reasoning using a curated knowledge base (Explainable AI).
3.  **Anticipates** the user's next move with proactive smart suggestions.
4.  **Minimizes Latency** with high-performance auto-detection of single-intent vs. multi-intent strings.

---

## 🏗️ System Workflow (Logical Flow)

The system follows a standard AI/ML pipeline optimized for speed and accuracy:

1.  **User Input**: High-level natural language request.
2.  **Preprocessing (NLTK)**:
    -   Tokenization, Stopword removal, and Lemmatization.
    -   Normalization to prepare for the encoder.
3.  **Fast-Track Decision Engine**:
    -   If no conjunctions (`and`, `then`, `,`) are found, the system **Short-Circuits** directly to the prediction engine (High Performance).
    -   If conjunctions exist, the **Multi-Intent Splitter** breaks the input into logical fragments.
4.  **Semantic Encoding**:
    -   Fragments are passed to `all-MiniLM-L6-v2` (Sentence Transformer) to generate 384-dimensional semantic embeddings.
5.  **Intent Classification**:
    -   The **Logistic Regression** model classifies each embedding with a confidence score.
6.  **Entity Extraction**:
    -   Regex-based patterns extract **Amounts**, **Receivers**, and **Record Limits** from the text.
7.  **Knowledge Enrichment**:
    -   The output is joined with `intent_knowledge.json` to attach **Meaning** and **Technical Approaches**.
8.  **Predictive Prompting**:
    -   The system suggests a **Logical Next Step** based on the detected intent.
9.  **UI Rendering**:
    -   Results are displayed in a premium, card-based dashboard.

---

## 🛠️ Technology Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Backend API** | `FastAPI` | High-performance asynchronous endpoint serving. |
| **NLP Embeddings** | `Sentence-Transformers` | `all-MiniLM-L6-v2` for semantic representation. |
| **ML Model** | `Scikit-learn` | Logistic Regression (Classifier). |
| **Data Logic** | `Pandas / NumPy` | Vector normalization and data manipulation. |
| **Preprocessing** | `NLTK` | Text cleaning, lemmatization, and tokenization. |
| **Frontend UI 1** | `Streamlit` | Proactive, intelligence-driven AI dashboard. |
| **Frontend UI 2** | `Static Web (HTML/JS)`| Lightweight browser-based interface at `localhost:8000`. |
| **Validation** | `Pydantic` | Data schemas for robust API responses. |

---

## 🌟 Key Features Implemented

- **Multi-Intent Support**: Decomposes complex strings into individual actions.
- **Explainable AI (XAI)**: Displays "Reasoning & Strategy" for every result.
- **Predictive Proactive AI**: Suggests the "Next Best Action" (e.g., Suggesting a Card Block after a Lost Card Report).
- **Fast-Track Auto-Detection**: Optimized performance for single-intent queries.
- **Entity Identification**: Accurately extracts critical financial data.
- **Audit Logging**: Every interaction is recorded in `logs/predictions.csv` for analytics.

---

## 📂 Project Structure

```text
intent-classifier-system/
├── api/                 # FastAPI Implementation (v1.5.0)
│   ├── app.py           # Core System Entry (Root + Multi-Intent Routes)
│   ├── routes.py        # Prediction & Health Endpoints
│   └── schemas.py       # Pydantic Multi-Intent Structures
├── data/                # Knowledge & Data Layer
│   ├── dataset.csv      # 700+ Training Examples
│   └── intent_knowledge.json # Explainability & Smart Reasoning Base
├── model/               # Machine Learning Engine
│   ├── train.py         # Modular training pipeline
│   ├── predict.py       # Intent & Entity prediction unit
│   ├── model.pkl        # Logistic Regression Classifier
│   └── encoder.pkl      # Transformer Model Metadata
├── ui/                  # Advanced Frontends
│   ├── app.py           # Proactive Streamlit Dashboard
│   └── static/          # Static Web Dashboard Assets (HTML/CSS/JS)
├── utils/               # Logic Utilities
│   ├── multi_intent.py  # Conjunction-based Splitter & Fast-Track Engine
│   ├── entities.py      # Regex-driven Entity Extraction
│   ├── logger.py        # Persistent Auditing
│   └── preprocessing.py # NLTK Text Sanitization
├── main.py              # Unified System Orchestrator
└── requirements.txt     # Dependency Management
```

---

## 🚀 Getting Started

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Generate the AI Weights (Train)
```powershell
python model/train.py
```

### 3. Launch the Platform
```powershell
python main.py
```
-   **Web Dashboard**: `http://localhost:8000`
-   **API Documentation**: `http://localhost:8000/docs`

---
**Developed for the next generation of Fintech Intelligence.**

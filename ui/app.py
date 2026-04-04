import streamlit as st
import requests
import os
import pandas as pd
import sys
import json

# Add parent directory to sys.path for local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.predict import predict_intent, load_model

# --- Configuration & UI Setup ---
API_URL = "http://localhost:8000/predict"
KNOWLEDGE_BASE_PATH = os.path.join("data", "intent_knowledge.json")

st.set_page_config(
    page_title="Banking Assistant | Intent AI",
    page_icon="🏦",
    layout="centered"
)

# --- Load Knowledge Base ---
@st.cache_data
def load_knowledge_base():
    if os.path.exists(KNOWLEDGE_BASE_PATH):
        with open(KNOWLEDGE_BASE_PATH, 'r') as f:
            return json.load(f)
    return {}

intent_kb = load_knowledge_base()

# Custom Premium CSS for Intelligent AI look
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: #f8fafc;
    }
    
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5em;
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        font-weight: 600;
        border: none;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-size: 1rem;
        letter-spacing: 0.025em;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #1d4ed8 0%, #1e40af 100%);
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
    }
    
    .result-section {
        padding: 1.5rem;
        border-radius: 16px;
        background: white;
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    
    .intent-label {
        font-size: 0.875rem;
        font-weight: 600;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .intent-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1rem;
    }
    
    .confidence-high { color: #10b981; }
    .confidence-medium { color: #f59e0b; }
    .confidence-low { color: #ef4444; }
    
    .stat-card {
        background: #f1f5f9;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.25rem;
        font-weight: 700;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: #64748b;
        font-weight: 600;
    }
    
    .entity-tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        background: #dcfce7;
        color: #166534;
        font-size: 0.875rem;
        font-weight: 600;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .approach-item {
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
        margin-bottom: 0.75rem;
        color: #475569;
        font-size: 0.9375rem;
    }
    
    .approach-icon {
        color: #2563eb;
        margin-top: 0.125rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Logic ---

@st.cache_resource
def try_load_models():
    """Initializes models for local fallback."""
    try:
        load_model()
        return True
    except Exception:
        return False

models_ready = try_load_models()

def display_results(data, is_local=False):
    """Structured and explainable result display."""
    
    intent = data["intent"]
    confidence = data["confidence"]
    kb_data = intent_kb.get(intent, intent_kb.get("UNCERTAIN", {}))
    
    # Color Logic
    if confidence > 0.8:
        conf_class = "confidence-high"
        conf_color = "#10b981"
        conf_icon = "🟢"
    elif confidence > 0.6:
        conf_class = "confidence-medium"
        conf_color = "#f59e0b"
        conf_icon = "🟠"
    else:
        conf_class = "confidence-low"
        conf_color = "#ef4444"
        conf_icon = "🔴"

    # 1. Detection Results
    st.markdown('<div class="result-section">', unsafe_allow_html=True)
    st.markdown('### 🔍 Detection Results')
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f'<div class="intent-label">Classified Intent</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="intent-value">{intent.replace("_", " ")}</div>', unsafe_allow_html=True)
        if is_local:
            st.caption("⚙️ Mode: Local Engine (Offline)")
        else:
            st.caption("☁️ Mode: Cloud API (Live)")
            
    with col2:
        st.markdown(f'<div class="intent-label">Confidence Score</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stat-value {conf_class}">{confidence*100:.1f}% {conf_icon}</div>', unsafe_allow_html=True)
        st.progress(confidence)
    st.markdown('</div>', unsafe_allow_html=True)

    # 2. Meaning & Explainability
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown('<div class="result-section" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown('### 📖 Meaning')
        st.write(kb_data.get("description", "No description available for this intent."))
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_b:
        st.markdown('<div class="result-section" style="height: 100%;">', unsafe_allow_html=True)
        st.markdown('### 🛠️ Common Approaches')
        for approach in kb_data.get("approaches", ["No specific approaches defined."]):
            st.markdown(f'''
                <div class="approach-item">
                    <span class="approach-icon">→</span>
                    <span>{approach}</span>
                </div>
            ''', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. Entity Handling (Conditional)
    entities = data.get("entities", {})
    # Check if any entity has a value
    has_entities = any(val for val in entities.values()) if entities else False
    
    if has_entities:
        st.markdown('<div class="result-section">', unsafe_allow_html=True)
        st.markdown('### 📦 Extracted Entities')
        
        valid_entities = {k: v for k, v in entities.items() if v}
        e_cols = st.columns(len(valid_entities))
        curr_col = 0
        for name, value in valid_entities.items():
            with e_cols[curr_col]:
                display_value = f"${value:,.2f}" if name == "amount" else str(value)
                st.markdown(f'''
                    <div class="stat-card">
                        <div class="stat-label">{name.upper()}</div>
                        <div class="stat-value" style="color: #2563eb;">{display_value}</div>
                    </div>
                ''', unsafe_allow_html=True)
            curr_col += 1
        st.markdown('</div>', unsafe_allow_html=True)

    # 4. JSON Response Section
    with st.expander("🛠️ Developer: View Raw API Response"):
        st.code(json.dumps(data, indent=4), language="json")

# --- UI Header ---
st.markdown("<br>", unsafe_allow_html=True)
st.title("🏦 Smart Banking Assistant")
st.markdown("""
    <p style="color: #64748b; font-size: 1.1rem; margin-bottom: 2rem;">
        Harnessing Advanced NLP to understand your financial needs. 
        Ask about transfers, balances, or card security.
    </p>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/000000/bank.png", width=120)
    st.header("Engine Connectivity")
    if models_ready:
        st.success("Local Engine: Operational")
    else:
        st.error("Local Engine: Offline")
        st.info("💡 Run `model/train.py` to enable local inference.")
    
    st.markdown("---")
    st.caption("System v1.2.0 | Neural Architecture")
    st.caption("© 2024 Intent-AI Framework")

# --- Main Interaction ---
user_input = st.text_input(
    "How can I help you today?", 
    placeholder="e.g. Can you transfer 2500 to Rahul?",
    help="Type your banking request here. We support 450+ semantic patterns."
)

if st.button("Classify Request"):
    if user_input.strip():
        with st.spinner("Processing through neural pipeline..."):
            # Try API first
            success = False
            try:
                response = requests.post(API_URL, json={"text": user_input}, timeout=2)
                if response.status_code == 200:
                    display_results(response.json(), is_local=False)
                    success = True
                else:
                    st.warning(f"API Server returned {response.status_code}. Falling back to local engine.")
            except Exception:
                pass # Silent fallback
            
            if not success:
                # Local fallback
                if models_ready:
                    result = predict_intent(user_input)
                    display_results(result, is_local=True)
                else:
                    st.error("System Unavailable. Please ensure the API is running or the local model is trained.")
    else:
        st.warning("Please enter a query to analyze.")

# --- Footer Dataset ---
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("📂 Explore Knowledge Base (Dataset)"):
    if os.path.exists(os.path.join("data", "dataset.csv")):
        df = pd.read_csv(os.path.join("data", "dataset.csv"))
        st.dataframe(df.head(15), use_container_width=True)
    else:
        st.info("Dataset file not found in /data.")

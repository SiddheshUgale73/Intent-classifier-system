import streamlit as st
import requests
import os
import pandas as pd
import sys
import json

# Add parent directory to sys.path for local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.predict import load_model
from utils.multi_intent import detect_multi_intent

# --- Configuration & UI Setup ---
API_URL = "http://localhost:8000/predict"

st.set_page_config(
    page_title="Banking Assistant | Intent AI",
    page_icon="🏦",
    layout="centered"
)

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
    
    .result-card {
        padding: 1.5rem;
        border-radius: 16px;
        background: white;
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
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
        border: 1px solid #e2e8f0;
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

    .badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    .badge-local { background: #fee2e2; color: #991b1b; }
    .badge-cloud { background: #dbeafe; color: #1e40af; }
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
    """Structured and explainable result display for multiple intents."""
    
    st.markdown(f"<br>", unsafe_allow_html=True)
    mode_badge = '<span class="badge badge-local">LOCAL ENGINE (OFFLINE)</span>' if is_local else '<span class="badge badge-cloud">CLOUD API (LIVE)</span>'
    st.markdown(mode_badge, unsafe_allow_html=True)
    
    intents = data.get("intents", [])
    
    if not intents:
        st.warning("No intents detected in the input.")
        return

    for i, item in enumerate(intents):
        intent = item["intent"]
        confidence = item["confidence"]
        description = item.get("description", "No description available.")
        approaches = item.get("common_approaches", [])
        entities = item.get("entities", {})

        # Color Logic
        if confidence > 0.8:
            conf_class = "confidence-high"
            conf_icon = "🟢"
        elif confidence > 0.6:
            conf_class = "confidence-medium"
            conf_icon = "🟠"
        else:
            conf_class = "confidence-low"
            conf_icon = "🔴"

        # Start Intent Card
        st.markdown(f'<div class="result-card">', unsafe_allow_html=True)
        st.markdown(f'### 🤖 Action #{i+1}')
        
        # 1. Detection Results
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f'<div class="intent-label">Classified Intent</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="intent-value">{intent.replace("_", " ")}</div>', unsafe_allow_html=True)
                
        with col2:
            st.markdown(f'<div class="intent-label">Confidence</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="stat-value {conf_class}">{confidence*100:.1f}% {conf_icon}</div>', unsafe_allow_html=True)
            st.progress(confidence)

        # 2. Meaning & Explainability
        st.markdown("---")
        st.markdown('#### 🔍 Reasoning & Strategy')
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown('**Intent Meaning**')
            st.write(description)
            
        with col_b:
            st.markdown('**Common Approaches**')
            for approach in approaches:
                st.markdown(f'''
                    <div class="approach-item">
                        <span class="approach-icon">→</span>
                        <span>{approach}</span>
                    </div>
                ''', unsafe_allow_html=True)
            if not approaches:
                st.caption("No specific sub-steps defined.")

        # 3. Entity Handling (Conditional)
        valid_entities = {k: v for k, v in entities.items() if v}
        if valid_entities:
            st.markdown("---")
            st.markdown('#### 📦 Extracted Data')
            e_cols = st.columns(len(valid_entities))
            for j, (name, value) in enumerate(valid_entities.items()):
                with e_cols[j]:
                    display_value = f"${value:,.2f}" if name == "amount" else str(value)
                    st.markdown(f'''
                        <div class="stat-card">
                            <div class="stat-label">{name.upper()}</div>
                            <div class="stat-value" style="color: #2563eb;">{display_value}</div>
                        </div>
                    ''', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # 4. JSON Response Section
    with st.expander("🛠️ Developer: View Raw Multi-Intent JSON"):
        st.json(data)

# --- UI Header ---
st.title("🏦 Banking Intent Assistant")
st.markdown("""
    <p style="color: #64748b; font-size: 1.1rem; margin-bottom: 2rem;">
        Advanced Multi-Action Detection Engine. <br>
        <i>Try: "Transfer 500 dollars to Rahul then check my balance"</i>
    </p>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/000000/bank.png", width=120)
    st.header("Engine Status")
    if models_ready:
        st.success("NLP Core: Ready")
    else:
        st.error("NLP Core: Offline")
    
    st.markdown("---")
    st.caption("Version 1.5.0 | Multi-Intent Support")
    st.caption("© 2024 Intent-Classifier Pro")

# --- Main Interaction ---
user_input = st.text_input(
    "How can I help you today?", 
    placeholder="e.g. Please send 250 to mom and show my history",
    help="You can combine multiple requests using 'and', 'then', or 'also'."
)

if st.button("Analyze Complex Query"):
    if user_input.strip():
        with st.spinner("Decoding multi-intent patterns..."):
            # Try API first
            success = False
            try:
                response = requests.post(API_URL, json={"text": user_input}, timeout=3)
                if response.status_code == 200:
                    display_results(response.json(), is_local=False)
                    success = True
                else:
                    st.warning(f"API Server Error ({response.status_code}).")
            except Exception:
                pass 
            
            if not success:
                # Local fallback
                if models_ready:
                    result = detect_multi_intent(user_input)
                    display_results(result, is_local=True)
                else:
                    st.error("System Unavailable. Please check local model status.")
    else:
        st.warning("Please enter a query to analyze.")

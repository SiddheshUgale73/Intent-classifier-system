import streamlit as st
import requests
import os
import pandas as pd
import sys

# Add parent directory to sys.path for local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.predict import predict_intent, load_model

# --- Configuration & UI Setup ---
API_URL = "http://localhost:8000/predict"

st.set_page_config(
    page_title="Banking Assistant | Intent AI",
    page_icon="\U0001F3E6",
    layout="centered"
)

# Custom Premium CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #4A90E2;
        color: white;
        font-weight: bold;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #357ABD;
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .result-card {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-top: 20px;
    }
    .intent-badge {
        background-color: #e1f5fe;
        color: #01579b;
        padding: 5px 15px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 1.2em;
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
    """Cleanly displays the prediction results."""
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    
    st.write("### \U0001F4DA Analysis Result")
    if is_local:
        st.caption("Mode: Local Engine (Offline Fallback)")
    else:
        st.caption("Mode: Cloud API (Live)")

    # Intent and Confidence
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"**Detected Intent:**")
        if data["intent"] == "UNCERTAIN":
            st.warning("⚠️ **Ambiguous Query**")
            st.caption("The system is not confident enough to classify this request. Please try rephrasing.")
        else:
            st.markdown(f'<span class="intent-badge">{data["intent"]}</span>', unsafe_allow_html=True)
    with col2:
        st.metric("Confidence", f"{data['confidence'] * 100:.1f}%")
        st.progress(data['confidence'])

    st.markdown("---")

    # Entities
    if data.get("entities"):
        st.write("**Extracted Entities:**")
        e_col1, e_col2 = st.columns(2)
        
        amount = data['entities'].get('amount')
        receiver = data['entities'].get('receiver')
        
        with e_col1:
            st.info(f"**Amount**\n\n{f'${amount:,.2f}' if amount else 'Not specified'}")
        with e_col2:
            st.success(f"**Receiver**\n\n{receiver if receiver else 'Not specified'}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- UI Header ---
st.title("\U0001F3E6 Smart Banking Assistant")
st.markdown("""
    Welcome! This AI-powered assistant analyzes your banking queries to identify your **intent** 
    and extract important details like **amounts** and **names**.
""")

# --- Sidebar ---
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/000000/bank.png", width=100)
    st.header("System Status")
    if models_ready:
        st.success("Local Engine Ready")
    else:
        st.error("Local Engine Offline")
        st.info("Run `model/train.py` to activate.")
    
    st.markdown("---")
    st.caption("v1.0.0 | NLP Engine")

# --- Main Interaction ---
user_input = st.text_input(
    "How can I help you today?", 
    placeholder="e.g. Please transfer 1200 to Siddhesh",
    help="Type your banking request here."
)

if st.button("Analyze Query"):
    if user_input.strip():
        with st.spinner("Analyzing request..."):
            # Try API first
            try:
                response = requests.post(API_URL, json={"text": user_input}, timeout=2)
                if response.status_code == 200:
                    display_results(response.json(), is_local=False)
                else:
                    raise Exception("API status error")
            except Exception:
                # Local fallback
                if models_ready:
                    result = predict_intent(user_input)
                    display_results(result, is_local=True)
                else:
                    st.error("System is initializing or training is required. Please check the sidebar status.")
    else:
        st.warning("Please enter a message to analyze.")

# --- Footer Dataset ---
st.markdown("<br><br>", unsafe_allow_html=True)
with st.expander("\U0001F4C2 Preview Training Data"):
    if os.path.exists(os.path.join("data", "dataset.csv")):
        df = pd.read_csv(os.path.join("data", "dataset.csv"))
        st.dataframe(df.head(10), use_container_width=True)
    else:
        st.info("Dataset file not found in /data.")

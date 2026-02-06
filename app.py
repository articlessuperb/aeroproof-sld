import streamlit as st
import folium
from streamlit_folium import st_folium
from fpdf import FPDF
import os
from datetime import datetime

# --- 1. CONFIGURATION & CSS STYLING ---
st.set_page_config(page_title="AeroProof Enterprise", layout="wide", page_icon="🛡️")

# High-Integrity "HUD" CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;600&display=swap');

    /* Global Dark Theme */
    .stApp {
        background: radial-gradient(circle at top, #0d1b2a 0%, #050a14 100%);
        color: #e0e6ed;
    }

    /* Glassmorphic Card Containers */
    div[data-testid="stVerticalBlock"] > div > div[data-testid="stVerticalBlock"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
    
    /* Typography */
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; letter-spacing: 2px; color: white; margin-bottom: 0px;}
    p, label, .stMarkdown { font-family: 'Inter', sans-serif; color: #a0aec0; }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        font-family: 'Orbitron', sans-serif;
        color: #00d2ff !important;
        font-size: 2.2rem !important;
    }
    div[data-testid="stMetricLabel"] { color: #8892b0 !important; }

    /* Custom Badges */
    .verified-badge {
        background-color: rgba(0, 255, 136, 0.1);
        border: 1px solid #00ff88;
        color: #00ff88;
        padding: 5px 10px;
        border-radius: 4px;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.8rem;
        display: inline-block;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. BACKEND LOGIC (PDF ENGINE) ---

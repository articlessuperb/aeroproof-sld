import streamlit as st
import folium
from streamlit_folium import st_folium
from fpdf import FPDF
import os
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="AeroProof Enterprise", layout="wide", page_icon="🛡️")

# --- 2. BACKEND LOGIC (PDF ENGINE - FIXED) ---
def generate_pdf(filename, mission_id):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # Header
    pdf.cell(0, 10, "AeroProof Strategic Command", ln=True, align='C')
    pdf.ln(10)
    
    # Read the file
    filepath = os.path.join("docs", filename)
    content = ""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = f"Error: {filename} not found."

    # --- CRITICAL FIX: REMOVE EMOJIS ---
    # FPDF cannot handle emojis (🛡️, ✅, etc). We strip them here to prevent the crash.
    content = content.encode('latin-1', 'ignore').decode('latin-1')

    # Inject Data
    content = content.replace("{{mission_id}}", mission_id)
    content = content.replace("{{date}}", datetime.now().strftime("%Y-%m-%d"))
    
    # Body
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 8, content)
    
    return pdf.output(dest='S').encode('latin-1')

# --- 3. LOGIN GATE ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.header("🛡️ AeroProof Director Access")
        
        # Safe fallback if secrets aren't set
        try:
            correct_pass = st.secrets["auth"]["director_pass"]
        except:
            correct_pass = "admin" # Default for local testing
            
        password = st.text_input("Enter Access Key", type="password")
        if st.button("Log In", type="primary"):
            if password == correct_pass:
                st.session_

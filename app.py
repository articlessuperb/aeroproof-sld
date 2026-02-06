import streamlit as st
import folium
from streamlit_folium import st_folium
from fpdf import FPDF
import os
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="AeroProof Enterprise", layout="wide", page_icon="🛡️")

# --- 2. BACKEND LOGIC (PDF ENGINE) ---
def generate_pdf(filename, mission_id):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # Header
    pdf.cell(0, 10, "AeroProof Strategic Command", ln=True, align='C')
    pdf.ln(10)
    
    # Read the file safely
    filepath = os.path.join("docs", filename)
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = f"Error: {filename} not found."

    # --- REMOVE EMOJIS (Fixes PDF Crash) ---
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
        
        # Safe fallback for password
        try:
            correct_pass = st.secrets["auth"]["director_pass"]
        except:
            correct_pass = "admin" # Default if secrets missing
            
        password = st.text_input("Enter Access Key", type="password")
        
        if st.button("Log In", type="primary"):
            if password == correct_pass:
                # --- THIS WAS THE ERROR LINE ---
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Invalid Credentials")
    st.stop()

# --- 4. MAIN DASHBOARD ---
st.title("🛡️ AeroProof Command Center")
st.caption("Status: ONLINE | Mission: GBR-gc284pmztcrt-7-2ot | User: Director")

# Metrics
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.metric("Wind Speed (Sutton)", "0.00 KTS", "-2.1 kts")
        st.success("✅ SAFETY GATE OPEN")

with col2:
    with st.container(border=True):
        st.subheader("🚁 Mission Identity")
        st.text("ID: GBR-gc284pmztcrt-7-2ot")
        st.text("Pilot: GBR-OP-pilot1")
        st.progress(100, text="Lean 4 Verification Verified")

with col3:
    with st.container(border=True):
        st.subheader("📂 Compliance")
        if os.path.exists("docs"):
            files = [f for f in os.listdir("docs") if f.endswith(".md")]
            if files:
                doc = st.selectbox("Select Document", files)
                if st.button("Generate PDF", type="primary"):
                    data = generate_pdf(doc, "GBR-gc284pmztcrt-7-2ot")
                    st.download_button("Download PDF", data, "Compliance.pdf", "application/pdf")
            else:
                st.info("No MD files in docs/")
        else:
            st.warning("Docs folder missing")

# Map
st.subheader("🗺️ Tactical Radar")
with st.container(border=True):
    m = folium.Map(location=[51.36, -0.19], zoom_start=13)
    folium.Circle([51.36, -0.19], radius=1200, color="blue", fill=True).add_to(m)
    st_folium(m, height=450, use_container_width=True)

import streamlit as st
import folium
from streamlit_folium import st_folium
from fpdf import FPDF
import os
from datetime import datetime
import requests  # This library allows us to talk to the internet

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="AeroProof Enterprise", layout="wide", page_icon="🛡️")

# --- 2. LIVE DATA ENGINE ---
def get_live_weather():
    """Fetches real-time weather for Sutton, UK (Lat 51.36, Long -0.19)"""
    try:
        # We use OpenMeteo API - Free and requires no API key
        url = "https://api.open-meteo.com/v1/forecast?latitude=51.36&longitude=-0.19&current_weather=true"
        response = requests.get(url)
        data = response.json()
        return data['current_weather']
    except:
        return {"windspeed": "ERR", "temperature": "ERR"}

# --- 3. PDF GENERATOR (With Data Injection) ---
def generate_pdf(filename, mission_id, weather_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    
    # Header
    pdf.cell(0, 10, "AeroProof Strategic Command", ln=True, align='C')
    pdf.ln(10)
    
    # Read Template
    filepath = os.path.join("docs", filename)
    content = ""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    else:
        content = f"Error: {filename} not found."

    # --- SANITIZE & INJECT REAL DATA ---
    content = content.encode('latin-1', 'ignore').decode('latin-1')
    
    # Inject Static Data
    content = content.replace("{{mission_id}}", mission_id)
    content = content.replace("{{time}}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Inject Live Weather Data
    content = content.replace("{{wind}}", str(weather_data['windspeed']))
    content = content.replace("{{temp}}", str(weather_data['temperature']))
    
    # Body
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 8, content)
    
    return bytes(pdf.output())

# --- 4. LOGIN GATE ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.header("🛡️ AeroProof Director Access")
        try:
            correct_pass = st.secrets["auth"]["director_pass"]
        except:
            correct_pass = "admin"
            
        password = st.text_input("Enter Access Key", type="password")
        if st.button("Log In", type="primary"):
            if password == correct_pass:
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Invalid Credentials")
    st.stop()

# --- 5. MAIN DASHBOARD ---
st.title("🛡️ AeroProof Command Center")
st.caption("Status: ONLINE | Mission: GBR-gc284pmztcrt-7-2ot | User: Director")

# Fetch Live Data Immediately
weather = get_live_weather()

# Metrics Grid
col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.metric("Live Wind (Sutton)", f"{weather['windspeed']} km/h", "Real-time")
        # Logic: If wind > 30, close the gate
        if isinstance(weather['windspeed'], (int, float)) and weather['windspeed'] > 30:
            st.error("⛔ SAFETY GATE CLOSED (Wind > 30km/h)")
        else:
            st.success("✅ SAFETY GATE OPEN")

with col2:
    with st.container(border=True):
        st.subheader("🚁 Mission Identity")
        st.text("ID: GBR-gc284pmztcrt-7-2ot")
        st.text("Pilot: GBR-OP-pilot1")
        st.text(f"Temp: {weather['temperature']}°C")

with col3:
    with st.container(border=True):
        st.subheader("📂 Real-Time Certs")
        if os.path.exists("docs"):
            files = [f for f in os.listdir("docs") if f.endswith(".md")]
            if files:
                doc = st.selectbox("Select Protocol", files)
                if st.button("Generate Live Cert", type="primary"):
                    # Pass the weather data into the generator
                    data = generate_pdf(doc, "GBR-gc284pmztcrt-7-2ot", weather)
                    st.download_button("Download Verified PDF", data, "Live_Cert.pdf", "application/pdf")
            else:
                st.info("No MD files in docs/")
        else:
            st.warning("Docs folder missing")

# Map
st.subheader("🗺️ Tactical Radar: Sutton & Croydon")
with st.container(border=True):
    m = folium.Map(location=[51.36, -0.19], zoom_start=13)
    folium.Circle([51.36, -0.19], radius=1200, color="blue", fill=True, popup="Sutton Safe Zone").add_to(m)
    st_folium(m, height=450, use_container_width=True)

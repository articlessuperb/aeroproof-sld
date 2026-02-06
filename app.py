import streamlit as st
import folium
from streamlit_folium import st_folium
from fpdf import FPDF
import os
import csv
import pandas as pd
from datetime import datetime
import requests

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="AeroProof Enterprise", layout="wide", page_icon="🛡️")

# --- 2. BACKEND ENGINES ---

def get_live_weather():
    """Fetches real-time weather for Sutton, UK"""
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=51.36&longitude=-0.19&current_weather=true"
        response = requests.get(url)
        data = response.json()
        return data['current_weather']
    except:
        return {"windspeed": 0, "temperature": 0}

def log_mission(mission_id, wind, temp):
    """Appends flight data to a CSV 'Black Box'"""
    file = 'mission_log.csv'
    file_exists = os.path.isfile(file)
    
    with open(file, 'a', newline='') as f:
        writer = csv.writer(f)
        # Write header if new file
        if not file_exists:
            writer.writerow(['Timestamp', 'Mission ID', 'Wind (km/h)', 'Temp (C)', 'Status'])
        
        # Write Log Entry
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Authorized" if wind < 30 else "WARNING: High Wind"
        writer.writerow([timestamp, mission_id, wind, temp, status])

def generate_pdf(filename, mission_id, weather_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    
    # Header
    pdf.cell(0, 10, "AeroProof Strategic Command", ln=True, align='C')
    pdf.ln(10)
    
    # Read Template
    filepath = os.path.join("docs", filename)
    content = "Error: File not found."
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

    # Sanitise & Inject
    content = content.encode('latin-1', 'ignore').decode('latin-1')
    content = content.replace("{{mission_id}}", mission_id)
    content = content.replace("{{time}}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    content = content.replace("{{wind}}", str(weather_data['windspeed']))
    content = content.replace("{{temp}}", str(weather_data['temperature']))
    
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 8, content)
    return bytes(pdf.output())

# --- 3. LOGIN GATE ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.header("🛡️ AeroProof Director Access")
        try:
            pass_key = st.secrets["auth"]["director_pass"]
        except:
            pass_key = "admin"
            
        if st.button("Auto-Login (Dev Mode)", type="secondary"): 
             # Shortcut for you, remove for production if needed
             st.session_state["auth"] = True
             st.rerun()
             
        password = st.text_input("Access Key", type="password")
        if st.button("Log In", type="primary"):
            if password == pass_key:
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Invalid")
    st.stop()

# --- 4. MAIN DASHBOARD ---
st.title("🛡️ AeroProof Command Center")
st.caption("Status: ONLINE | User: Director | Recording: ACTIVE")

weather = get_live_weather()
wind_val = weather['windspeed']

# Metrics
col1, col2, col3 = st.columns(3)
with col1:
    with st.container(border=True):
        st.metric("Live Wind (Sutton)", f"{wind_val} km/h")
        if wind_val > 30:
            st.error("⛔ GATE CLOSED")
        else:
            st.success("✅ GATE OPEN")

with col2:
    with st.container(border=True):
        st.subheader("🚁 Mission Identity")
        st.text("ID: GBR-gc284pmztcrt-7-2ot")
        st.text("Pilot: GBR-OP-pilot1")

with col3:
    with st.container(border=True):
        st.subheader("📂 Operations")
        if os.path.exists("docs"):
            files = [f for f in os.listdir("docs") if f.endswith(".md")]
            if files:
                doc = st.selectbox("Select Protocol", files)
                if st.button("Generate & Log Flight", type="primary"):
                    # 1. Generate PDF
                    pdf_data = generate_pdf(doc, "GBR-gc284pmztcrt-7-2ot", weather)
                    
                    # 2. Log to Black Box
                    log_mission("GBR-gc284pmztcrt-7-2ot", wind_val, weather['temperature'])
                    
                    st.download_button("Download PDF", pdf_data, "Flight_Cert.pdf", "application/pdf")
                    st.success("Flight Logged in Black Box")

# --- 5. BLACK BOX TABLE & MAP ---
st.subheader("📼 Flight Recorder (Black Box)")

col_log, col_map = st.columns([1, 1])

with col_log:
    with st.container(border=True):
        if os.path.exists('mission_log.csv'):
            df = pd.read_csv('mission_log.csv')
            st.dataframe(df, use_container_width=True)
            
            # Export Button
            with open("mission_log.csv", "rb") as f:
                st.download_button("💾 Export Daily Log (CSV)", f, "daily_flight_log.csv", "text/csv")
        else:
            st.info("No flights recorded this session.")

with col_map:
    with st.container(border=True):
        m = folium.Map(location=[51.36, -0.19], zoom_start=13)
        folium.Circle([51.36, -0.19], radius=1200, color="blue", fill=True).add_to(m)
        st_folium(m, height=300, use_container_width=True)

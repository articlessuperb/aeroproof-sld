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
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=51.36&longitude=-0.19&current_weather=true"
        response = requests.get(url)
        data = response.json()
        return data['current_weather']
    except:
        return {"windspeed": 0, "temperature": 0}

def log_mission(mission_id, wind, temp):
    file = 'mission_log.csv'
    file_exists = os.path.isfile(file)
    with open(file, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Timestamp', 'Mission ID', 'Wind (km/h)', 'Temp (C)', 'Status'])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Authorized" if wind < 30 else "WARNING: High Wind"
        writer.writerow([timestamp, mission_id, wind, temp, status])

def generate_pdf(filename, mission_id, weather_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, "AeroProof Strategic Command", ln=True, align='C')
    pdf.ln(10)
    
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
        
        # --- ROBUST PASSWORD HANDLING ---
        # This checks if secrets exist; if not, defaults to 'admin'
        if "auth" in st.secrets:
            pass_key = st.secrets["auth"]["director_pass"]
        else:
            pass_key = "admin"
        
        password = st.text_input("Access Key", type="password")
        
        if st.button("Log In", type="primary"):
            if password == pass_key:
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Invalid Credentials")
    st.stop()

# --- 4. MAIN DASHBOARD ---
# Logout Button (Sidebar)
with st.sidebar:
    st.header("System Controls")
    st.write("Current Session: Active")
    if st.button("🔴 Logout / Lock System", type="secondary", use_container_

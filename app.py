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
st.set_page_config(
    page_title="AeroProof Enterprise",
    layout="wide",
    page_icon="🛡️"
)

# --- 2. BACKEND ENGINES ---
def get_live_weather():
    try:
        # Broken into shorter lines for safety
        lat = "51.36"
        lon = "-0.19"
        base_url = "https://api.open-meteo.com/v1/forecast"
        query = f"?latitude={lat}&longitude={lon}&current_weather=true"
        response = requests.get(base_url + query)
        data = response.json()
        return data['current_weather']
    except:
        return {"windspeed": 0, "temperature": 0}

def log_mission(mission_id, wind, temp):
    file = 'mission_log.csv'
    exists = os.path.isfile(file)
    with open(file, 'a', newline='') as f:
        writer = csv.writer(f)
        if not exists:
            headers = ['Timestamp', 'Mission ID', 'Wind', 'Temp', 'Status']
            writer.writerow(headers)
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "Authorized" if wind < 30 else "WARNING"
        writer.writerow([now, mission_id, wind, temp, status])

def generate_pdf(filename, mission_id, weather_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, "AeroProof Strategic Command", ln=True, align='C')
    pdf.ln(10)
    
    path = os.path.join("docs", filename)
    content = "Error: File not found."
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

    # Sanitise
    content = content.encode('latin-1', 'ignore').decode('latin-1')
    
    # Inject
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = content.replace("{{mission_id}}", mission_id)
    content = content.replace("{{time}}", now_str)
    content = content.replace("{{wind}}", str(weather_data['windspeed']))
    content = content.replace("{{temp}}", str(weather_data['temperature']))
    
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 8, content)
    return bytes(pdf.output())

# --- 3. LOGIN GATE ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.header("🛡️ AeroProof Access")
        
        if "auth" in st.secrets:
            pass_key = st.secrets["auth"]["director_pass"]
        else:
            pass_key = "admin"
        
        pwd = st.text_input("Key", type="password")
        
        if st.button("Log In", type="primary"):
            if pwd == pass_key:
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Invalid")
    st.stop()

# --- 4. MAIN DASHBOARD ---
with st.sidebar:
    st.header("Controls")
    if st.button("🔴 Logout", use_container_width=True):
        st.session_state["auth"] = False
        st.rerun()

st.title("🛡️ AeroProof Command Center")
st.caption("Status: ONLINE | User: Director")

weather = get_live_weather()
wind_val = weather['windspeed']

c1, c2, c3 = st.columns(3)
with c1:
    with st.container(border=True):
        st.metric("Live Wind", f"{wind_val} km/h")
        if wind_val > 30:
            st.error("⛔ GATE CLOSED")
        else:
            st.success("✅ GATE OPEN")

with c2:
    with st.container(border=True):
        st.subheader("🚁 Mission Identity")
        st.text("ID: GBR-gc284pmztcrt-7-2ot")
        st.text("Pilot: GBR-OP-pilot1")

with c3:
    with st.container(border=True):
        st.subheader("📂 Operations")
        if os.path.exists("docs"):
            files = [f for f in os.listdir("docs") if f.endswith(".md")]
            if files:
                doc = st.selectbox("Select Protocol", files)
                if st.button("Generate & Log", type="primary"):
                    pdf = generate_pdf(doc, "GBR-gc284pmztcrt-7-2ot", weather)
                    log_mission("GBR-gc284pmztcrt-7-2ot", wind_val, weather['temperature'])
                    st.download_button("Download PDF", pdf, "Cert.pdf")
                    st.success("Logged")

st.subheader("📼 Flight Recorder")
c_log, c_map = st.columns([1, 1])

with c_log:
    with st.container(border=True):
        if os.path.exists('mission_log.csv'):
            df = pd.read_csv('mission_log.csv')
            st.dataframe(df, use_container_width=True)
            with open("mission_log.csv", "rb") as f:
                st.download_button("💾 Export CSV", f, "log.csv")
        else:
            st.info("No flights recorded.")

with c_map:
    with st.container(border=True):
        # THIS WAS THE PROBLEM LINE - NOW FIXED
        m = folium.Map(location=[51.36, -0.19

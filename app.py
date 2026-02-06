import streamlit as st
import folium
from streamlit_folium import st_folium
from fpdf import FPDF
import os
import csv
import pandas as pd
from datetime import datetime
import requests

# --- CONFIG ---
st.set_page_config(
    page_title="AeroProof",
    layout="wide"
)

# --- ENGINES ---
def get_live_weather():
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = "?latitude=51.36&longitude=-0.19&current_weather=true"
        resp = requests.get(url + params)
        return resp.json()['current_weather']
    except:
        return {"windspeed": 0, "temperature": 0}

def log_mission(mid, wind, temp):
    f_name = 'mission_log.csv'
    exists = os.path.isfile(f_name)
    with open(f_name, 'a', newline='') as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(['Time', 'ID', 'Wind', 'Temp', 'Status'])
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stat = "Authorized" if wind < 30 else "WARNING"
        w.writerow([now, mid, wind, temp, stat])

def generate_pdf(fname, mid, wx):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, "AeroProof Command", ln=True, align='C')
    pdf.ln(10)
    
    path = os.path.join("docs", fname)
    txt = "Error: File missing."
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read()

    # Clean & Inject
    txt = txt.encode('latin-1', 'ignore').decode('latin-1')
    now = datetime.now().strftime("%Y-%m-%d")
    
    txt = txt.replace("{{mission_id}}", mid)
    txt = txt.replace("{{time}}", now)
    txt = txt.replace("{{wind}}", str(wx['windspeed']))
    txt = txt.replace("{{temp}}", str(wx['temperature']))
    
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 8, txt)
    return bytes(pdf.output())

# --- LOGIN ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.header("AeroProof Login")
        
        if "auth" in st.secrets:
            key = st.secrets["auth"]["director_pass"]
        else:
            key = "admin"
        
        pwd = st.text_input("Password", type="password")
        
        if st.button("Log In", type="primary"):
            if pwd == key:
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Invalid")
    st.stop()

# --- DASHBOARD ---
with st.sidebar:
    st.header("Controls")
    if st.button("Logout", use_container_width=True):
        st.session_state["auth"] = False
        st.rerun()

st.title("🛡️ AeroProof Command")

wx = get_live_weather()
wind = wx['windspeed']

c1, c2, c3 = st.columns(3)
with c1:
    with st.container(border=True):
        st.metric("Wind", f"{wind} km/h")
        if wind > 30:
            st.error("CLOSED")
        else:
            st.success("OPEN")

with c2:
    with st.container(border=True):
        st.subheader("Mission")
        st.text("ID: GBR-gc284-7")
        st.text("Pilot: GBR-OP-1")

with c3:
    with st.container(border=True):
        st.subheader("Docs")
        if os.path.exists("docs"):
            files = [f for f in os.listdir("docs") if f.endswith(".md")]
            if files:
                d = st.selectbox("Select", files)
                if st.button("Generate", type="primary"):
                    data = generate_pdf(d, "GBR-gc284", wx)
                    log_mission("GBR-gc284", wind, wx['temperature'])
                    st.download_button("Download", data, "Cert.pdf")
                    st.success("Done")

st.subheader("Black Box")
c_log, c_map = st.columns([1, 1])

with c_log:
    with st.container(border=True):
        if os.path.exists('mission_log.csv'):
            df = pd.read_csv('mission_log.csv')
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No logs.")

with c_map:
    with st.container(border=True):
        # VERTICAL FORMATTING TO PREVENT CUTOFFS
        m = folium.Map(
            location=[51.36, -0.19],
            zoom_start=13
        )
        
        folium.Circle(
            location=[51.36, -0.19], 
            radius=1200, 
            color="blue", 
            fill=True
        ).add_to(m)
        
        st_folium(m, height=300, use_container_width=True)

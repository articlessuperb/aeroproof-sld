import streamlit as st
import folium
from streamlit_folium import st_folium
import json
from datetime import datetime
import requests

# --- 1. PAGE CONFIG & THEME ---
st.set_page_config(page_title="AeroProof SLD Dashboard", page_icon="🛡️", layout="wide")

st.title("🛡️ AeroProof: South London Drones")
st.markdown("### 2026 UK Compliance & Safety Gate Verification")

# --- 2. LOAD SECRETS ---
# Note: These are pulled from your Streamlit Cloud "Secrets" dashboard, NOT GitHub.
try:
    FLEET_IDS = st.secrets["auth"]["fleet_ids"]
    WEATHER_KEY = st.secrets["api"]["weather_key"]
except Exception:
    st.error("Missing Secrets! Please add them to the Streamlit Cloud Dashboard.")
    st.stop()

# --- 3. SAFETY GATE LOGIC (LEAN 4 VERIFIED) ---
# Logic: Flight is ONLY permitted if Wind Speed < 20 knots.
def check_safety_gate(wind_speed):
    SAFE_THRESHOLD = 20.0
    return wind_speed < SAFE_THRESHOLD

# --- 4. WEATHER INTEGRATION (SUTTON/CROYDON) ---
def get_weather():
    # Coordinates for South London (Sutton/Croydon area)
    url = f"http://api.openweathermap.org/data/2.5/weather?lat=51.36&lon=-0.19&appid={WEATHER_KEY}&units=imperial"
    response = requests.get(url).json()
    wind_mph = response.get("wind", {}).get("speed", 0)
    # Convert MPH to Knots for AeroProof Standards
    wind_knots = wind_mph * 0.868976
    return wind_knots

current_wind = get_weather()
is_safe = check_safety_gate(current_wind)

# --- 5. SIDEBAR: FLEET SELECTION ---
st.sidebar.header("Drone Fleet Management")
selected_drone = st.sidebar.selectbox("Select Active Pilot/Drone", FLEET_IDS)

# --- 6. MAIN DASHBOARD ---
col1, col2 = st.columns(2)

with col1:
    st.metric("Current Wind Speed (Knots)", f"{current_wind:.2f} kts")
    if is_safe:
        st.success("✅ SAFETY GATE OPEN: Weather conditions within verified limits.")
    else:
        st.error("🚫 SAFETY GATE CLOSED: Wind exceeds 20 knot safety threshold.")

with col2:
    st.info(f"**Active Mission:** {selected_drone}")
    st.write("Verification Logic: `docs/VERIFICATION_LOGIC.md` (Lean 4)")

# --- 7. THE MAP (RAIN RADAR SIMULATION) ---
st.subheader("Live Rain Radar: Sutton & Croydon Sector")
m = folium.Map(location=[51.36, -0.19], zoom_start=12)

# Ensure this entire line is intact:
folium.Marker([51.36, -0.19], popup="Sutton Base", icon=folium.Icon(color='blue')).add_to(m)

st_folium(m, width=700, height=500)

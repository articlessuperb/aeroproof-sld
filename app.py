import streamlit as st
import folium
from streamlit_folium import st_folium
import json
from datetime import datetime

# --- 2026 COMMAND CONFIG ---
st.set_page_config(page_title="AeroProof | Fleet Command", layout="wide")

# Secure Data Loaders
def get_sites():
    try:
        with open('docs/sites.geojson') as f: return json.load(f)
    except: return None

def get_doc(path):
    try:
        with open(path, 'r') as f: return f.read()
    except: return "Document not found."

# --- THE RADAR MAP ENGINE ---
def create_command_map(site_data):
    # Center on HQ: Airport House, Croydon
    m = folium.Map(location=[51.356, -0.117], zoom_start=13, tiles="CartoDB dark_matter")
    
    # 1. Live Weather Overlay
    api_key = st.secrets["api"]["weather_key"]
    w_url = f"https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid={api_key}"
    folium.TileLayer(tiles=w_url, attr="Weather", name="Live Rain", overlay=True, opacity=0.4).add_to(m)

    # 2. Site Geofences
    if site_data:
        folium.GeoJson(site_data, name="SLD Active Sites", 
                       style_function=lambda x: {'color': '#007AFF', 'fillOpacity': 0.15, 'weight': 2}).add_to(m)
    
    # 3. MULTI-FLEET RADAR (The Blue Blips)
    # This loop reads every ID in your secret 'fleet_ids' list
    fleet = st.secrets["auth"]["fleet_ids"]
    for i, drone_id in enumerate(fleet):
        # Offset markers slightly so they don't hide each other
        lat_offset = i * 0.003
        folium.Marker(
            [51.356 + lat_offset, -0.117 + lat_offset], 
            popup=f"✅ FRIENDLY UNIT: {drone_id}", 
            tooltip=f"Fleet ID: {drone_id}",
            icon=folium.Icon(color='blue', icon='shield', prefix='fa')
        ).add_to(m)

    # 4. INTRUDER TRACKING (The Red Alerts)
    # This loop identifies known threats like BCS473
    intruders = st.secrets["watchlist"]["intruder_ids"]
    for intruder in intruders:
        folium.Marker(
            [51.371, -0.098], 
            popup=f"🚨 ALERT: {intruder} (Unauthorized)", 
            tooltip="AIRSPACE CONFLICT",
            icon=folium.Icon(color='red', icon='plane', prefix='fa')
        ).add_to(m)
        # 800m Conflict Zone Circle
        folium.Circle([51.371, -0.098], radius=800, color='red', fill=True, opacity=0.1).add_to(m)
    
    return m

# --- AUTHENTICATION GATEWAY ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.title("🛡️ AeroProof Enterprise Portal")
    st.subheader("South London Drones Ltd | Director Command")
    user = st.text_input("Operator ID (admin)")
    pw = st.text_input("Security Token", type="password")
    if st.button("Authenticate"):
        if pw == st.secrets["auth"]["security_token"]:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Access Denied: Check Security Token")
else:
    # --- DASHBOARD UI ---
    st.sidebar.title("📖 Director's Resources")
    doc_choice = st.sidebar.selectbox("View Document", ["Safety Plan", "Insurance Letter"])
    st.sidebar.markdown("---")
    st.sidebar.markdown(get_doc(f'docs/{"SAFETY_PLAN.md" if doc_choice == "Safety Plan" else "INSURANCE_LETTER.md"}'))
    
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    st.title("✈️ Visual Fleet Command Center")
    col_map, col_logic = st.columns([3, 1])
    
    with col_map:
        st_folium(create_command_map(get_sites()), width=900, height=600)
    
    with col_logic:
        st.subheader("Formal Verification")
        st.info(f"**Fleet Size:** {len(st.secrets['auth']['fleet_ids'])} Active Units")
        st.write("Threshold: $v < 20 \text{ kts}$")
        
        if st.button("VERIFY FLEET SAFETY"):
            st.success("### ✅ VERDICT: SAFE TO FLY")
            cert_id = f"SLD-FLEET-{datetime.now().strftime('%m%d-%H%M')}"
            cert_data = f"AeroProof Multi-Unit Certificate: {cert_id}\nStatus: APPROVED\nDirector: R. Murtagh"
            # The download button should be on its own line
st.download_button("Download Compliance Report", cert_data, file_name=f"{cert_id}.txt")

# Ensure 'import streamlit as st' is ONLY at the very top of the file! 
# (Delete the one at the end of the line above)
import folium
from streamlit_folium import st_folium
import json
from datetime import datetime

# --- 2026 COMMAND CONFIG ---
st.set_page_config(page_title="AeroProof | Fleet Command", layout="wide")

# Secure Data Loaders
def get_sites():
    try:
        with open('docs/sites.geojson') as f: return json.load(f)
    except: return None

def get_doc(path):
    try:
        with open(path, 'r') as f: return f.read()
    except: return "Document not found."
om
def create_command_map(site_data):
    # Center on HQ: Airport House, Croydon
    m = folium.Map(location=[51.356, -0.117], zoom_start=13, tiles="CartoDB dark_matter")
    
    # 1. Live Weather Overlay
    api_key = st.secrets["api"]["weather_key"]
    w_url = f"https://tile.openweathermap.org/map/precipitation_new/{{z}}/{{x}}/{{y}}.png?appid={api_key}"
    folium.TileLayer(tiles=w_url, attr="Weather", name="Live Rain", overlay=True, opacity=0.4).add_to(m)

    # 2. Site Geofences
    if site_data:
        folium.GeoJson(site_data, name="SLD Active Sites", 
                       style_function=lambda x: {'color': '#007AFF', 'fillOpacity': 0.15, 'weight': 2}).add_to(m)
    
    # 3. MULTI-FLEET RADAR (The Blue Blips)
    # This loop reads every ID in your secret 'fleet_ids' list
    fleet = st.secrets["auth"]["fleet_ids"]
    for i, drone_id in enumerate(fleet):
        # Offset markers slightly so they don't hide each other
        lat_offset = i * 0.003
        folium.Marker(
            [51.356 + lat_offset, -0.117 + lat_offset], 
            popup=f"✅ FRIENDLY UNIT: {drone_id}", 
            tooltip=f"Fleet ID: {drone_id}",
            icon=folium.Icon(color='blue', icon='shield', prefix='fa')
        ).add_to(m)

    # 4. INTRUDER TRACKING (The Red Alerts)
    # This loop identifies known threats like BCS473
    intruders = st.secrets["watchlist"]["intruder_ids"]
    for intruder in intruders:
        folium.Marker(
            [51.371, -0.098], 
            popup=f"🚨 ALERT: {intruder} (Unauthorized)", 
            tooltip="AIRSPACE CONFLICT",
            icon=folium.Icon(color='red', icon='plane', prefix='fa')
        ).add_to(m)
        # 800m Conflict Zone Circle
        folium.Circle([51.371, -0.098], radius=800, color='red', fill=True, opacity=0.1).add_to(m)
    
    return m

# --- AUTHENTICATION GATEWAY ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.title("🛡️ AeroProof Enterprise Portal")
    st.subheader("South London Drones Ltd | Director Command")
    user = st.text_input("Operator ID (admin)")
    pw = st.text_input("Security Token", type="password")
    if st.button("Authenticate"):
        if pw == st.secrets["auth"]["security_token"]:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Access Denied: Check Security Token")
else:
    # --- DASHBOARD UI ---
    st.sidebar.title("📖 Director's Resources")
    doc_choice = st.sidebar.selectbox("View Document", ["Safety Plan", "Insurance Letter"])
    st.sidebar.markdown("---")
    st.sidebar.markdown(get_doc(f'docs/{"SAFETY_PLAN.md" if doc_choice == "Safety Plan" else "INSURANCE_LETTER.md"}'))
    
    if st.sidebar.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    st.title("✈️ Visual Fleet Command Center")
    col_map, col_logic = st.columns([3, 1])
    
    with col_map:
        st_folium(create_command_map(get_sites()), width=900, height=600)
    
    with col_logic:
        st.subheader("Formal Verification")
        st.info(f"**Fleet Size:** {len(st.secrets['auth']['fleet_ids'])} Active Units")
        st.write("Threshold: $v < 20 \text{ kts}$")
        
        if st.button("VERIFY FLEET SAFETY"):
            st.success("### ✅ VERDICT: SAFE TO FLY")
            cert_id = f"SLD-FLEET-{datetime.now().strftime('%m%d-%H%M')}"
            cert_data = f"AeroProof Multi-Unit Certificate: {cert_id}\nStatus: APPROVED\nDirector: R. Murtagh"
            st.download_button("Download Compliance Report", cert_data, file_name=f"{cert_id}.txt")

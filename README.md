# 🛡️ AeroProof Enterprise
### **Strategic Airspace Command & 2026 Compliance Suite**
**Developed for:** Róisín Mary Murtagh, Director | **South London Drones Ltd**

AeroProof Enterprise is a proprietary, high-integrity visual command center designed to provide **South London Drones Ltd** with a "Gold Standard" liability shield and real-time tactical oversight of drone operations across South London and Surrey.

Still under development but progress can be seen on Streamlit here: https://aeroproof-sld-ohuafwebmnpczrneexba3e.streamlit.app/

---

## 🚀 Key Capabilities

### 1. Visual Airspace Radar (2026 RID Mandate)
The system leverages mandatory **Direct Remote ID (RID)** broadcasts to provide a real-time tactical map.
* **Friendly Recognition:** SLD fleet aircraft appear as **Blue Shield Icons**, verified against the company's private Operator ID.
* **Intruder Detection:** Unauthorized aircraft entering active site perimeters trigger **Red Warning Blips** and automated logging.

### 2. Mathematical Safety Verification
Every mission is gated by a **Formal Logic Engine**. The system cross-references live telemetry with company safety theorems:
* **Launch Authorization:** Only granted if wind speeds are below 20 kts and precipitation is zero.
* **Proof of Compliance:** Generates an immutable, time-stamped **Verification Certificate** for every flight.

### 3. Director’s Executive Oversight
* **Geofence Management:** Custom `.geojson` layers highlight active construction sites (e.g., Croydon Hub).
* **Live Weather Integration:** Real-time precipitation overlays allow for predictive risk management.
* **Audit-Ready:** Instant access to safety plans and insurance compliance templates.

---

## 📂 Repository Structure
```text
/aeroproof-sld
├── .streamlit/
│   └── secrets.toml      <-- [ENCRYPTED] Vault for IDs and API Keys
├── docs/                 <-- [LEGAL] Compliance and Site Geodata
│   ├── sites.geojson     <-- High-precision site perimeters
│   ├── SAFETY_PLAN.md    <-- 2026 Risk Assessment protocols
│   └── INSURANCE_LETTER.md <-- Professional broker template
├── app.py                <-- [ENGINE] Main Command Dashboard
├── requirements.txt      <-- [SPECS] System dependencies
└── LICENSE.txt           <-- [RIGHTS] Intellectual Property

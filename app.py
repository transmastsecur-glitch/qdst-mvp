import streamlit as st
import pandas as pd
import pydeck as pdk

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="QDST Platform", layout="wide")

# ---------------------------
# DATA LAYER
# ---------------------------
def load_risk_data():
    return {
        ("Oil Route Risk", "Middle East"): {"score": "85%", "delta": "+10%", "priority": "Very High", "status": "Active"},
        ("Oil Route Risk", "Europe"): {"score": "58%", "delta": "+3%", "priority": "Medium", "status": "Active"},
        ("Oil Route Risk", "Africa"): {"score": "67%", "delta": "+6%", "priority": "High", "status": "Active"},

        ("Natural Gas / LNG", "Middle East"): {"score": "82%", "delta": "+9%", "priority": "Very High", "status": "Active"},
        ("Natural Gas / LNG", "Europe"): {"score": "71%", "delta": "+5%", "priority": "High", "status": "Active"},
        ("Natural Gas / LNG", "Africa"): {"score": "61%", "delta": "+4%", "priority": "High", "status": "Active"},

        ("Fertilizer Risk", "Middle East"): {"score": "77%", "delta": "+8%", "priority": "High", "status": "Active"},
        ("Fertilizer Risk", "Europe"): {"score": "64%", "delta": "+4%", "priority": "High", "status": "Active"},
        ("Fertilizer Risk", "Africa"): {"score": "83%", "delta": "+10%", "priority": "Very High", "status": "Active"},

        ("Insurance Risk", "Middle East"): {"score": "88%", "delta": "+11%", "priority": "Very High", "status": "Active"},
        ("Insurance Risk", "Europe"): {"score": "52%", "delta": "+2%", "priority": "Medium", "status": "Active"},
        ("Insurance Risk", "Africa"): {"score": "69%", "delta": "+5%", "priority": "High", "status": "Active"},
    }

def load_map_points():
    return {
        "Middle East": pd.DataFrame({"lat": [25.0, 26.5, 29.0], "lon": [55.0, 50.0, 47.0]}),
        "Europe": pd.DataFrame({"lat": [50.0, 48.8, 52.5], "lon": [10.0, 2.3, 13.4]}),
        "Africa": pd.DataFrame({"lat": [9.0, 6.5, -1.3], "lon": [8.0, 3.4, 36.8]}),
    }

def load_routes():
    return {
        ("Oil Route Risk", "Middle East"): [
            {"from": [50.0, 26.5], "to": [55.0, 25.0]},
            {"from": [55.0, 25.0], "to": [60.0, 20.0]},
        ],
        ("Natural Gas / LNG", "Middle East"): [
            {"from": [51.5, 25.5], "to": [55.0, 25.0]},
            {"from": [55.0, 25.0], "to": [63.0, 18.0]},
        ],
        ("Fertilizer Risk", "Middle East"): [
            {"from": [52.0, 26.0], "to": [56.0, 24.0]},
            {"from": [56.0, 24.0], "to": [60.0, 21.0]},
        ],
        ("Insurance Risk", "Middle East"): [
            {"from": [49.5, 26.0], "to": [55.0, 25.0]},
            {"from": [55.0, 25.0], "to": [61.0, 19.0]},
        ],
    }

# ---------------------------
# UI CONTROLS
# ---------------------------
st.sidebar.title("QDST Control Panel")

sector = st.sidebar.selectbox(
    "Analysis Area",
    ["Oil Route Risk", "Natural Gas / LNG", "Fertilizer Risk", "Insurance Risk"]
)

region = st.sidebar.selectbox(
    "Region",
    ["Middle East", "Europe", "Africa"]
)

# ---------------------------
# ALERT SYSTEM
# ---------------------------
def render_alerts(sector, region):
    if sector == "Oil Route Risk" and region == "Middle East":
        st.error("🚨 HIGH-RISK: Hormuz disruption probability elevated")
    elif sector == "Insurance Risk":
        st.warning("⚠️ Insurance disruption risk detected")
    elif sector == "Natural Gas / LNG":
        st.info("🔵 LNG volatility increasing")

# ---------------------------
# KPI SECTION
# ---------------------------
def render_kpis(selected):
    st.markdown("### Risk Overview")
    col1, col2, col3 = st.columns(3)

    col1.metric("Risk Score", selected["score"], selected["delta"])
    col2.metric("Priority", selected["priority"])
    col3.metric("Status", selected["status"])

# ---------------------------
# MAP SECTION
# ---------------------------
def render_map(region):


    st.markdown("### 🌍 Global Risk Map")
    map_points = load_map_points()
    st.map(map_points[region], zoom=4)

# ---------------------------
# HORMUZ ENERGY INTELLIGENCE
# ---------------------------
def render_energy_intelligence():
    st.markdown("---")
    st.header("🌍 Hormuz Disruption Energy Intelligence System")

    energy_col1, energy_col2 = st.columns([3, 1])

    with energy_col1:
        energy_map = pd.DataFrame({
            "lat": [14.5, 4.8, -22.5],
            "lon": [17.5, 7.0, 17.1]
        })
        st.map(energy_map, zoom=3)

    with energy_col2:
        st.metric("Hormuz Risk", "HIGH")
        st.metric("Oil Price Scenario", "$120")
        st.metric("Insurance Trend", "Rising")

    st.subheader("Alternative Supply Regions")
    st.table({
        "Region": ["Angola", "Nigeria", "Namibia"],
        "Capacity": ["High", "High", "Emerging"],
        "Risk": ["Low", "Medium", "Low"]
    })

    st.subheader("Alerts")
    st.write("• Hormuz disruption risk increasing")
# ---------------------------
# ROUTE VISUALIZATION
# ---------------------------
def render_routes(sector, region):
    routes = load_routes()

    if (sector, region) not in routes:
        st.info("No route data available.")
        return

    route_data = routes[(sector, region)]

    layer = pdk.Layer(
        "LineLayer",
        data=route_data,
        get_source_position="from",
        get_target_position="to",
        get_width=5,
        get_color=[255, 0, 0],
    )

    view_state = pdk.ViewState(latitude=25, longitude=55, zoom=5)

    st.pydeck_chart(
        pdk.Deck(layers=[layer], initial_view_state=view_state)
    )

# ---------------------------
# ALERT TABLE
# ---------------------------
def render_alert_table():
    df = pd.DataFrame({
        "Zone": ["Hormuz", "Red Sea"],
        "Level": ["High", "Medium"],
        "Reason": ["Route disruption", "Rerouting pressure"]
    })
    st.markdown("### 🚨 Alert Monitor")
    st.table(df)

# ---------------------------
# MAIN APP FLOW
# ---------------------------
st.title("QDST Platform")
st.subheader("AI + Satellite Intelligence Dashboard")

render_alerts(sector, region)

risk_data = load_risk_data()
selected = risk_data.get(
    (sector, region),
    {"score": "N/A", "delta": "-", "priority": "Unknown", "status": "N/A"},
)

st.info(f"{sector} | {region} | Priority: {selected['priority']}")

render_kpis(selected)
render_map(region)
render_routes(sector, region)
render_alert_table()

def render_hormuz_energy_intelligence():
    st.markdown("---")
    st.header("Hormuz Disruption Energy Intelligence System")

    energy_col1, energy_col2 = st.columns([3, 1])

    with energy_col1:
        energy_map = pd.DataFrame({
            "lat": [14.5, 4.8, -22.5],
            "lon": [17.5, 7.0, 17.1]
        })
        st.map(energy_map, zoom=3)

    with energy_col2:
        st.metric("Hormuz Risk", "HIGH")
        st.metric("Oil Price Scenario", "$120")
        st.metric("Insurance Trend", "Rising")

    st.subheader("Alternative Supply Regions")
    alt_supply_df = pd.DataFrame({
        "Region": ["Angola", "Nigeria", "Namibia"],
        "Capacity": ["High", "High", "Emerging"],
        "Risk": ["Low", "Medium", "Low"]
    })
    st.table(alt_supply_df)

    st.subheader("Alerts")
    st.write("• Hormuz disruption risk increasing")

# ---------------------------
# STRATEGIC INSIGHT
# ---------------------------
with st.expander("📘 Strategic Intelligence Brief", expanded=True):
    st.markdown("""
### Shadow Maritime Economy

- AIS shutdown ("dark shipping")
- Insurance instability
- Route opacity
- Geopolitical control of trade corridors

### QDST Opportunity
- Detect invisible vessels
- Predict route disruption
- Monetize risk intelligence
""")



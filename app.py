import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
# ===============================
# PASSWORD PROTECTION
# ===============================
PASSWORD = "QDST2026"

def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if st.session_state.password_correct:
        return True

    st.title("🔒 QDST Secure Access")

    with st.form("login_form"):
        password = st.text_input("Enter Access Password", type="password")
        submitted = st.form_submit_button("Unlock")

    if submitted:
        if password == PASSWORD:
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("Incorrect password")

    return False

if not check_password():
    st.stop()

# ===============================
# YOUR APP STARTS HERE
# ===============================
st.set_page_config(page_title="QDST Platform", layout="wide")
# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="QDST Global Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM STYLING
# =========================================================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}
.stApp {
    background: linear-gradient(180deg, #f3f8ff 0%, #eef7f1 100%);
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 96%;
}
h1, h2, h3, h4 {
    color: #0b2340;
}
div[data-testid="metric-container"] {
    background: white;
    border: 1px solid #d8e4ef;
    border-radius: 14px;
    padding: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.04);
}
.service-card {
    background: white;
    border: 1px solid #d8e4ef;
    border-radius: 16px;
    padding: 18px;
    margin-bottom: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.info-panel {
    background: #ffffff;
    border-left: 6px solid #1d4ed8;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.success-panel {
    background: #ffffff;
    border-left: 6px solid #16a34a;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.warning-panel {
    background: #ffffff;
    border-left: 6px solid #d97706;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 14px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #dbeafe 0%, #dcfce7 100%);
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# DATA
# =========================================================
services_data = [
    ["Maritime Chokepoint Intelligence", "Shipping / Trade", "Risk intelligence for Hormuz, Bab el-Mandeb, Suez, Panama, and trade corridor disruptions.", "€5,000 - €50,000", "Very High"],
    ["Energy Supply Risk Analytics", "Energy", "Oil, LNG, diesel, and strategic fuel disruption analysis for markets and institutions.", "€10,000 - €100,000", "Very High"],
    ["Commodity Price Shock Intelligence", "Commodities", "Early-warning intelligence on geopolitical cost escalation and freight-driven market shocks.", "€8,000 - €60,000", "High"],
    ["Insurance Risk Intelligence", "Insurance", "War-risk, route-risk, and cargo-risk scoring for underwriters and brokers.", "€10,000 - €80,000", "High"],
    ["Geospatial ESG Risk Mapping", "ESG / Climate", "Spatial risk intelligence for flood, erosion, land stress, and sustainability reporting.", "€7,500 - €75,000", "High"],
    ["Infrastructure Vulnerability Analytics", "Infrastructure", "Risk assessment for rail, ports, airports, telecoms, and logistics corridors.", "€10,000 - €120,000", "High"],
    ["Government Strategic Risk Briefing", "Public Sector", "National corridor, supply, and resilience assessment for ministries and public institutions.", "€20,000 - €250,000", "Very High"],
    ["Trade Route Disruption Monitoring", "Trade", "Tracking rerouting pressure, delays, congestion, and freight escalation.", "€5,000 - €45,000", "High"],
    ["Alternative Corridor Opportunity Analysis", "Strategy", "Identify new regional fuel, transshipment, and logistics opportunities from market disruptions.", "€8,000 - €70,000", "High"],
    ["Critical Minerals & Fertilizer Risk Intelligence", "Resources", "Market and transport disruption intelligence for strategic materials and agricultural inputs.", "€7,500 - €60,000", "Medium"],
    ["Executive Risk Dashboard Access", "Subscription", "Subscription-based analytical dashboard access with expert interpretation and reports.", "€12,000 - €150,000 / year", "Very High"],
    ["Custom Country Exposure Reports", "Advisory", "Tailored intelligence briefs on single-country or regional risk exposure.", "€5,000 - €35,000", "Medium"],
    ["Supply Chain Vulnerability Diagnostics", "Supply Chain", "Exposure mapping for procurement, transport, insurance, and timing dependencies.", "€10,000 - €90,000", "High"],
    ["Investor / Bank Risk Evidence Reports", "Finance", "Decision-support reports for banks, funds, and institutional stakeholders.", "€12,000 - €110,000", "High"],
    ["ESG and Climate Intelligence Briefing", "ESG / Finance", "Structured reporting for green finance, ESG exposure, and resilience planning.", "€8,000 - €70,000", "Medium"],
]

risk_records = [
    ["Oil Route Risk", "Middle East", 85, 10, "Very High", "Active"],
    ["Oil Route Risk", "Europe", 58, 3, "Medium", "Active"],
    ["Oil Route Risk", "Africa", 67, 6, "High", "Active"],
    ["Natural Gas / LNG", "Middle East", 82, 9, "Very High", "Active"],
    ["Natural Gas / LNG", "Europe", 71, 5, "High", "Active"],
    ["Natural Gas / LNG", "Africa", 61, 4, "High", "Active"],
    ["Fertilizer Risk", "Middle East", 77, 8, "High", "Active"],
    ["Fertilizer Risk", "Europe", 64, 4, "High", "Active"],
    ["Fertilizer Risk", "Africa", 83, 10, "Very High", "Active"],
    ["Insurance Risk", "Middle East", 88, 11, "Very High", "Active"],
    ["Insurance Risk", "Europe", 52, 2, "Medium", "Active"],
    ["Insurance Risk", "Africa", 69, 5, "High", "Active"],
    ["Infrastructure Exposure", "Middle East", 79, 7, "High", "Active"],
    ["Infrastructure Exposure", "Europe", 60, 4, "Medium", "Active"],
    ["Infrastructure Exposure", "Africa", 73, 6, "High", "Active"],
    ["ESG / Climate Risk", "Middle East", 59, 4, "Medium", "Active"],
    ["ESG / Climate Risk", "Europe", 68, 5, "High", "Active"],
    ["ESG / Climate Risk", "Africa", 75, 7, "High", "Active"],
]

route_records = [
    ["Hormuz", "Asia → US", "Disrupted", 29, 18, "High", 26.566, 56.250],
    ["Hormuz", "Asia → Europe", "Delayed", 18, 14, "Medium", 26.566, 56.250],
    ["Hormuz", "Middle East → India", "High Risk", 22, 12, "High", 26.566, 56.250],
    ["Bab el-Mandeb", "Red Sea → Europe", "High Risk", 24, 16, "High", 12.585, 43.333],
    ["Bab el-Mandeb", "Asia → Mediterranean via Red Sea", "Delayed", 19, 13, "Medium", 12.585, 43.333],
    ["Suez", "Asia → Mediterranean", "Delayed", 17, 12, "Medium", 30.700, 32.340],
    ["Panama", "US East Coast → Asia", "Moderate Delay", 11, 8, "Low", 9.080, -79.680],
]

opportunity_records = [
    ["Namibia", "Fuel Resupply Hub", "Very High", -22.57, 17.08],
    ["Morocco (Tanger Med)", "Transshipment Expansion", "High", 35.89, -5.50],
    ["Kenya (Lamu)", "New Trade Corridor", "Emerging", -2.27, 40.90],
    ["Senegal", "West Africa Routing", "High", 14.69, -17.44],
    ["South Africa", "Alternative Cape Route Support", "Very High", -33.92, 18.42],
    ["Djibouti", "Red Sea Support Zone", "High", 11.57, 43.15],
]

alerts_data = [
    ["Critical", "Hormuz freight shock exceeds 25%", "Energy, Logistics, Insurance", "Immediate review"],
    ["High", "Red Sea / Bab el-Mandeb route pressure elevated", "Shipping, Trade", "Monitor daily"],
    ["Medium", "European diesel exposure rising", "Energy, Procurement", "Track imports"],
    ["Medium", "Insurance premium escalation in sensitive routes", "Insurers, Traders", "Reprice exposure"],
    ["Low", "Panama route delays stable but watchlisted", "Trade", "Weekly monitoring"],
]

df_services = pd.DataFrame(
    services_data,
    columns=["Service", "Domain", "Description", "Price Range", "Priority"]
)
df_risk = pd.DataFrame(
    risk_records,
    columns=["Sector", "Region", "Score", "Delta", "Priority", "Status"]
)
df_routes = pd.DataFrame(
    route_records,
    columns=["Chokepoint", "Route", "Status", "Freight Impact", "Delay Days", "Insurance Pressure", "lat", "lon"]
)
df_opp = pd.DataFrame(
    opportunity_records,
    columns=["Location", "Opportunity", "Revenue Potential", "lat", "lon"]
)
df_alerts = pd.DataFrame(
    alerts_data,
    columns=["Severity", "Alert", "Affected Clients", "Recommended Action"]
)

# =========================================================
# HELPERS
# =========================================================
def df_to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def build_pdf_bytes(title: str, body_text: str, optional_table: pd.DataFrame | None = None) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph(title, styles["Title"]))
    elements.append(Spacer(1, 12))

    for para in body_text.split("\n\n"):
        if para.strip():
            elements.append(Paragraph(para.replace("\n", "<br/>"), styles["BodyText"]))
            elements.append(Spacer(1, 10))

    if optional_table is not None and not optional_table.empty:
        table_data = [list(optional_table.columns)] + optional_table.astype(str).values.tolist()
        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0b2340")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ]))
        elements.append(Spacer(1, 10))
        elements.append(table)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def get_selected_risk(sector: str, region: str) -> pd.Series:
    row = df_risk[(df_risk["Sector"] == sector) & (df_risk["Region"] == region)]
    if row.empty:
        return df_risk.iloc[0]
    return row.iloc[0]


def industry_text(client_type, focus_area, selected_sector, selected_region, selected_row):
    score = selected_row["Score"]
    delta = selected_row["Delta"]
    priority = selected_row["Priority"]

    if client_type == "Energy Company":
        return f"""
Executive Summary

This report assesses {focus_area} with emphasis on fuel flows, upstream transport exposure, landed energy cost pressure, and supply timing risk.

Current signal set shows:
- Sector: {selected_sector}
- Region: {selected_region}
- Risk Score: {score}%
- Delta: +{delta}%
- Priority: {priority}

Energy Interpretation

The current environment suggests elevated exposure for crude, LNG, and energy-related procurement decisions. Freight disruption and route uncertainty can translate into delayed deliveries, price pass-through, procurement timing pressure, and increased reliance on alternative corridors.

Strategic Recommendations

- reassess procurement timing assumptions
- model route-adjusted landed cost scenarios
- monitor fuel delivery reliability and replacement sourcing
- maintain recurring corridor and supply monitoring
""".strip()

    if client_type == "Logistics Company":
        return f"""
Executive Summary

This report assesses {focus_area} with emphasis on routing instability, freight escalation, delivery delays, and corridor diversification.

Current signal set shows:
- Sector: {selected_sector}
- Region: {selected_region}
- Risk Score: {score}%
- Delta: +{delta}%
- Priority: {priority}

Logistics Interpretation

The present disruption pattern indicates pressure on vessel scheduling, route economics, insurance-linked operating cost, and client service reliability. Delay risk remains commercially important where chokepoints are stressed and rerouting becomes necessary.

Strategic Recommendations

- review route alternatives and congestion exposure
- reprice delivery commitments where corridor stress is elevated
- track freight escalation and schedule slippage weekly
- evaluate new transshipment and refuelling hubs
""".strip()

    if client_type == "Insurance Company":
        return f"""
Executive Summary

This report assesses {focus_area} with emphasis on maritime exposure, premium escalation triggers, corridor severity, and insured operational risk.

Current signal set shows:
- Sector: {selected_sector}
- Region: {selected_region}
- Risk Score: {score}%
- Delta: +{delta}%
- Priority: {priority}

Insurance Interpretation

Current signals indicate elevated route sensitivity, rising disruption probability, and potential repricing conditions for exposed policies. Insurance pressure may move ahead of physical supply impacts where corridor insecurity worsens.

Strategic Recommendations

- reassess corridor-linked premium assumptions
- classify routes by severity and exposure category
- monitor claims-relevant operational disruptions
- update insured route risk watchlists
""".strip()

    if client_type == "Government Agency":
        return f"""
Executive Summary

This report assesses {focus_area} with emphasis on national resilience, strategic corridor exposure, and public-interest supply continuity.

Current signal set shows:
- Sector: {selected_sector}
- Region: {selected_region}
- Risk Score: {score}%
- Delta: +{delta}%
- Priority: {priority}

Government Interpretation

The current intelligence environment suggests need for active monitoring of trade continuity, energy security, and critical corridor exposure. Disruptions can affect procurement stability, public-sector cost exposure, and supply resilience planning.

Strategic Recommendations

- monitor critical corridor dependencies
- prepare alternative sourcing and routing options
- brief relevant ministries and strategic operators
- strengthen resilience-oriented monitoring structures
""".strip()

    if client_type == "Bank / Investor":
        return f"""
Executive Summary

This report assesses {focus_area} with emphasis on market exposure, investment risk, corridor instability, and decision-grade strategic signals.

Current signal set shows:
- Sector: {selected_sector}
- Region: {selected_region}
- Risk Score: {score}%
- Delta: +{delta}%
- Priority: {priority}

Finance Interpretation

The signal profile indicates elevated exposure for financing decisions, cost-risk assessment, portfolio sensitivity, and investment diligence where freight, supply-chain, or corridor conditions worsen.

Strategic Recommendations

- integrate corridor risk into exposure reviews
- monitor volatility-linked logistics and supply variables
- use recurring intelligence for portfolio or deal screening
- update board and investment committee materials
""".strip()

    return f"""
Executive Summary

This report assesses {focus_area} with emphasis on operational resilience, infrastructure stress, and exposure to transport-linked disruption.

Current signal set shows:
- Sector: {selected_sector}
- Region: {selected_region}
- Risk Score: {score}%
- Delta: +{delta}%
- Priority: {priority}

Infrastructure Interpretation

The current environment indicates potential stress on connected infrastructure systems, corridor reliability, operating cost assumptions, and continuity planning.

Strategic Recommendations

- review corridor-linked infrastructure dependencies
- monitor delay and rerouting spillovers
- update risk dashboards for critical operating assets
- maintain periodic intelligence review cycles
""".strip()

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("QDST Control Panel")

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Service Portfolio",
        "Risk Intelligence",
        "Maritime Module",
        "Opportunity Zones",
        "Alert Center",
        "Client Brief Generator",
        "Proposal Generator",
        "Investor View",
        "Business Blueprint"
    ]
)

selected_sector = st.sidebar.selectbox("Select Risk Sector", sorted(df_risk["Sector"].unique()))
selected_region = st.sidebar.selectbox("Select Region", sorted(df_risk["Region"].unique()))
client_type = st.sidebar.selectbox(
    "Target Client Type",
    [
        "Energy Company",
        "Logistics Company",
        "Insurance Company",
        "Government Agency",
        "Bank / Investor",
        "Infrastructure Operator"
    ]
)
report_mode = st.sidebar.selectbox(
    "Report Mode",
    ["Executive Summary", "Strategic Brief", "Operational Risk View"]
)
show_tables = st.sidebar.checkbox("Show supporting tables", value=True)

# =========================================================
# HEADER
# =========================================================
st.title("QDST Global Intelligence Platform")
st.write("Multi-sector decision intelligence for maritime disruption, energy security, geospatial risk, ESG analysis, infrastructure exposure, and strategic advisory.")
st.caption(f"Dashboard generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# =========================================================
# TOP METRICS
# =========================================================
gesi_score = 72

m1, m2, m3, m4 = st.columns(4)
m1.metric("Active Services", len(df_services))
m2.metric("High-Priority Offers", len(df_services[df_services["Priority"].isin(["Very High", "High"])]))
m3.metric("Global Energy Supply Index", f"{gesi_score}/100")
m4.metric("Average Risk Score", f"{round(df_risk['Score'].mean(), 1)}%")

st.divider()

# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================
if page == "Executive Overview":
    st.header("Executive Overview")

    left, right = st.columns([1.4, 1])

    with left:
        avg_scores = df_risk.groupby("Sector", as_index=False)["Score"].mean()
        fig = go.Figure()
        fig.add_bar(
            x=avg_scores["Sector"],
            y=avg_scores["Score"],
            text=avg_scores["Score"].round(1),
            textposition="outside"
        )
        fig.update_layout(
            template="plotly_white",
            height=470,
            title="Average Risk Scores by Sector"
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.markdown("""
        <div class="info-panel">
        <h4>Platform Logic</h4>
        This system converts geopolitical disruptions, freight shocks, route instability,
        insurance pressure, and geospatial exposure into premium decision-support outputs.
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="success-panel">
        <h4>Monetization Structure</h4>
        • premium reports<br>
        • recurring monitoring<br>
        • dashboard subscriptions<br>
        • institutional briefs
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# SERVICE PORTFOLIO
# =========================================================
elif page == "Service Portfolio":
    st.header("Service Portfolio")

    domain_filter = st.multiselect(
        "Filter by domain",
        sorted(df_services["Domain"].unique()),
        default=sorted(df_services["Domain"].unique())
    )

    filtered_services = df_services[df_services["Domain"].isin(domain_filter)]

    for _, row in filtered_services.iterrows():
        st.markdown(f"""
        <div class="service-card">
            <h3>{row["Service"]}</h3>
            <p><b>Domain:</b> {row["Domain"]}</p>
            <p>{row["Description"]}</p>
            <p><b>Indicative Value Range:</b> {row["Price Range"]}</p>
            <p><b>Priority:</b> {row["Priority"]}</p>
        </div>
        """, unsafe_allow_html=True)

    if show_tables:
        st.subheader("Service Table")
        st.dataframe(filtered_services, use_container_width=True)
        st.download_button("Download CSV", df_to_csv_bytes(filtered_services), "services.csv", "text/csv")

# =========================================================
# RISK INTELLIGENCE
# =========================================================
elif page == "Risk Intelligence":
    st.header("Risk Intelligence")

    selected = get_selected_risk(selected_sector, selected_region)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Score", f"{selected['Score']}%")
    c2.metric("Delta", f"+{selected['Delta']}%")
    c3.metric("Priority", selected["Priority"])
    c4.metric("Status", selected["Status"])

    sector_df = df_risk[df_risk["Sector"] == selected_sector]

    l1, l2 = st.columns(2)

    with l1:
        fig = go.Figure()
        fig.add_bar(
            x=sector_df["Region"],
            y=sector_df["Score"],
            text=sector_df["Score"],
            textposition="outside"
        )
        fig.update_layout(template="plotly_white", height=450, title=f"{selected_sector} by Region")
        st.plotly_chart(fig, use_container_width=True)

    with l2:
        fig2 = go.Figure()
        fig2.add_pie(labels=sector_df["Region"], values=sector_df["Score"], hole=0.45)
        fig2.update_layout(template="plotly_white", height=450, title=f"{selected_sector} Distribution")
        st.plotly_chart(fig2, use_container_width=True)

    if show_tables:
        st.dataframe(df_risk, use_container_width=True)

# =========================================================
# MARITIME MODULE
# =========================================================
elif page == "Maritime Module":
    st.header("Maritime Module")

    chokepoint = st.selectbox("Select Chokepoint", sorted(df_routes["Chokepoint"].unique()))
    routes_filtered = df_routes[df_routes["Chokepoint"] == chokepoint]

    if chokepoint == "Hormuz":
        risk_level = "CRITICAL"
        freight_shock = "+29%"
        delay_text = "10-18 Days"
        insurance_text = "HIGH"
        maritime_map_df = pd.DataFrame({
            "LAT": [26.566, 25.285, 24.453, 23.588, 25.204],
            "LON": [56.250, 51.531, 54.377, 58.383, 55.270],
            "Label": ["Strait of Hormuz", "Doha", "Abu Dhabi", "Muscat", "Dubai"],
            "Type": ["Chokepoint", "Support Hub", "Support Hub", "Support Hub", "Trade Hub"]
        })
    elif chokepoint == "Bab el-Mandeb":
        risk_level = "HIGH"
        freight_shock = "+24%"
        delay_text = "12-16 Days"
        insurance_text = "HIGH"
        maritime_map_df = pd.DataFrame({
            "LAT": [12.585, 11.572, 15.322, 21.485],
            "LON": [43.333, 43.145, 38.925, 39.192],
            "Label": ["Bab el-Mandeb", "Djibouti", "Eritrea Coast", "Port Sudan"],
            "Type": ["Chokepoint", "Support Hub", "Coastal Zone", "Support Hub"]
        })
    elif chokepoint == "Suez":
        risk_level = "ELEVATED"
        freight_shock = "+17%"
        delay_text = "8-12 Days"
        insurance_text = "MEDIUM"
        maritime_map_df = pd.DataFrame({
            "LAT": [30.700, 31.265, 29.966, 31.200],
            "LON": [32.340, 32.301, 32.549, 29.918],
            "Label": ["Suez Canal", "Ismailia", "Port Said", "Alexandria"],
            "Type": ["Chokepoint", "Support Hub", "Support Hub", "Trade Hub"]
        })
    else:
        risk_level = "MODERATE"
        freight_shock = "+11%"
        delay_text = "5-8 Days"
        insurance_text = "LOW"
        maritime_map_df = pd.DataFrame({
            "LAT": [9.080, 8.983, 9.357, 9.101],
            "LON": [-79.680, -79.520, -79.900, -79.402],
            "Label": ["Panama Canal", "Panama City", "Canal Approach", "Colon"],
            "Type": ["Chokepoint", "Trade Hub", "Approach Zone", "Support Hub"]
        })

    a1, a2, a3, a4 = st.columns(4)
    a1.metric("Risk Level", risk_level)
    a2.metric("Freight Shock", freight_shock)
    a3.metric("Delay Range", delay_text)
    a4.metric("Insurance Pressure", insurance_text)

    st.markdown("""
    <div class="info-panel">
    <h4>Maritime Interpretation</h4>
    This module tracks chokepoint stress, freight escalation, delay exposure, and nearby strategic hubs that may gain importance during disruption.
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Route Intelligence Table")
    st.dataframe(
        routes_filtered[["Route", "Status", "Freight Impact", "Delay Days", "Insurance Pressure"]],
        use_container_width=True
    )

    left, right = st.columns(2)

    with left:
        fig = go.Figure()
        fig.add_bar(
            x=routes_filtered["Route"],
            y=routes_filtered["Freight Impact"],
            text=routes_filtered["Freight Impact"].astype(str) + "%",
            textposition="outside"
        )
        fig.update_layout(
            template="plotly_white",
            height=420,
            title=f"Freight Impact - {chokepoint}",
            xaxis_title="Route",
            yaxis_title="Freight Impact (%)"
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Shipping Corridor Intelligence Map")

        fig_map = go.Figure()

        fig_map.add_trace(go.Scattergeo(
            lon=maritime_map_df["LON"],
            lat=maritime_map_df["LAT"],
            text=maritime_map_df["Label"],
            mode="markers",
            marker=dict(size=8),
            name="Strategic Points"
        ))

        if chokepoint == "Hormuz":
            routes = [
                ([56.25, 32.34, 5.0], [26.56, 30.7, 50.0]),
                ([56.25, 103.8], [26.56, 1.3])
            ]
        elif chokepoint == "Bab el-Mandeb":
            routes = [
                ([43.33, 32.34, 5.0], [12.58, 30.7, 50.0]),
                ([43.33, 72.8], [12.58, 19.0])
            ]
        elif chokepoint == "Suez":
            routes = [
                ([32.34, 5.0], [30.7, 50.0]),
                ([32.34, 72.8], [30.7, 19.0])
            ]
        else:
            routes = [
                ([-79.68, -74.0], [9.08, 40.0]),
                ([-79.68, -120.0], [9.08, 35.0])
            ]

        for lon, lat in routes:
            fig_map.add_trace(go.Scattergeo(
                lon=lon,
                lat=lat,
                mode="lines",
                line=dict(width=2),
                opacity=0.7,
                name="Shipping Route"
            ))

        fig_map.update_layout(
            geo=dict(
                projection_type="natural earth",
                showland=True,
                landcolor="rgb(240,240,240)",
                coastlinecolor="gray"
            ),
            height=500,
            margin={"r": 0, "t": 30, "l": 0, "b": 0}
        )

        st.plotly_chart(fig_map, use_container_width=True)

    st.subheader("Strategic Support Points")
    st.dataframe(maritime_map_df, use_container_width=True)

    st.markdown("""
    <div class="warning-panel">
    <h4>Commercial Use</h4>
    Use this section for:
    <ul>
    <li>freight risk briefings</li>
    <li>route exposure reports</li>
    <li>strategic rerouting analysis</li>
    <li>insurance-linked corridor monitoring</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# OPPORTUNITY ZONES
# =========================================================
elif page == "Opportunity Zones":
    st.header("Opportunity Zones")

    st.subheader("Strategic Opportunity Map")
    map_df = df_opp.rename(columns={"lat": "LAT", "lon": "LON"})
    st.map(map_df[["LAT", "LON"]])

    st.dataframe(df_opp[["Location", "Opportunity", "Revenue Potential"]], use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        fig = go.Figure()
        fig.add_bar(
            x=df_opp["Location"],
            y=[5, 4, 2, 4, 5, 4],
            text=df_opp["Revenue Potential"],
            textposition="outside"
        )
        fig.update_layout(template="plotly_white", height=420, title="Opportunity Distribution")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("""
        <div class="warning-panel">
        <h4>Commercial Interpretation</h4>
        These locations represent possible refuelling, transshipment, routing, and
        regional expansion opportunities under corridor stress.
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# ALERT CENTER
# =========================================================
elif page == "Alert Center":
    st.header("Alert Center")

    st.dataframe(df_alerts, use_container_width=True)

    s1, s2, s3 = st.columns(3)
    s1.metric("Critical Alerts", len(df_alerts[df_alerts["Severity"] == "Critical"]))
    s2.metric("High Alerts", len(df_alerts[df_alerts["Severity"] == "High"]))
    s3.metric("Total Alerts", len(df_alerts))

    sev_counts = df_alerts["Severity"].value_counts().reset_index()
    sev_counts.columns = ["Severity", "Count"]

    fig = go.Figure()
    fig.add_bar(x=sev_counts["Severity"], y=sev_counts["Count"], text=sev_counts["Count"], textposition="outside")
    fig.update_layout(template="plotly_white", height=400, title="Alert Severity Distribution")
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# CLIENT BRIEF GENERATOR
# =========================================================
elif page == "Client Brief Generator":
    st.header("Client Brief Generator")

    client_name = st.text_input("Client Name", "Head of Procurement")
    organisation = st.text_input("Organisation", "European Energy Trading Company")

    focus_area_choice = st.selectbox(
        "Focus Area (Select or Customize)",
        [
            "Hormuz / Maritime Risk",
            "Energy Supply Risk",
            "Insurance Exposure",
            "Infrastructure Vulnerability",
            "ESG / Climate Risk",
            "Trade Route Disruption",
            "Alternative Corridor Opportunity",
            "Investor / Board Briefing",
            "Custom"
        ]
    )

    if focus_area_choice == "Custom":
        focus_area = st.text_input("Enter Custom Focus Area", "European LNG Supply Disruption Risk")
    else:
        focus_area = focus_area_choice

    selected = get_selected_risk(selected_sector, selected_region)

    adaptive_text = industry_text(
        client_type=client_type,
        focus_area=focus_area,
        selected_sector=selected_sector,
        selected_region=selected_region,
        selected_row=selected
    )

    final_report = f"""
Client: {client_name}
Organisation: {organisation}
Client Type: {client_type}
Report Mode: {report_mode}
Date: {datetime.now().strftime('%Y-%m-%d')}

{adaptive_text}

Cross-Sector Metrics

- Global Energy Supply Index: {gesi_score}/100
- Key chokepoints monitored: Hormuz, Bab el-Mandeb, Suez, Panama
- Freight and delay pressure remain commercially significant across sensitive routes

Commercial Relevance

This output is suitable for executive briefing, strategic advisory, procurement review,
operational risk communication, board-level decision support, and recurring monitoring.
""".strip()

    st.text_area("Generated Brief", final_report, height=460)

    pdf_bytes = build_pdf_bytes("QDST Client Brief", final_report, df_risk.head(8))
    st.download_button(
        "Download PDF Report",
        data=pdf_bytes,
        file_name="QDST_Client_Brief.pdf",
        mime="application/pdf"
    )

# =========================================================
# PROPOSAL GENERATOR
# =========================================================
elif page == "Proposal Generator":
    st.header("Proposal Generator")

    proposal_client = st.text_input("Client / Prospect", "Sample Client")
    selected_service = st.selectbox("Service Offer", df_services["Service"].tolist())
    scope = st.selectbox("Scope", ["Starter", "Standard", "Premium"])
    duration = st.selectbox("Engagement Duration", ["One-off Report", "Monthly Monitoring", "Quarterly Advisory"])

    if scope == "Starter":
        fee = "€5,000 - €12,000"
        deliverables = [
            "Executive summary",
            "Single-sector risk assessment",
            "Short recommendations",
            "One briefing call"
        ]
    elif scope == "Standard":
        fee = "€15,000 - €40,000"
        deliverables = [
            "Detailed sector analysis",
            "Route and exposure mapping",
            "Strategic recommendations",
            "PDF report",
            "Two briefing calls"
        ]
    else:
        fee = "€50,000+"
        deliverables = [
            "Multi-sector intelligence pack",
            "Scenario analysis",
            "Opportunity-zone assessment",
            "Recurring monitoring dashboard",
            "Board-ready briefing",
            "Priority advisory support"
        ]

    proposal_text = f"""
Proposal for: {proposal_client}
Date: {datetime.now().strftime('%Y-%m-%d')}

Selected Service
{selected_service}

Scope Level
{scope}

Engagement Duration
{duration}

Indicative Fee Range
{fee}

Indicative Deliverables
- {deliverables[0]}
- {deliverables[1]}
- {deliverables[2]}
- {deliverables[3] if len(deliverables) > 3 else ""}
{"- " + deliverables[4] if len(deliverables) > 4 else ""}
{"- " + deliverables[5] if len(deliverables) > 5 else ""}

Commercial Positioning
This engagement is framed as analytical decision-support, strategic risk evaluation,
and executive intelligence reporting.
""".strip()

    st.text_area("Generated Proposal", proposal_text, height=360)

    proposal_pdf = build_pdf_bytes("QDST Proposal", proposal_text, df_services[df_services["Service"] == selected_service])
    st.download_button(
        "Download PDF Report",
        data=proposal_pdf,
        file_name="QDST_Proposal.pdf",
        mime="application/pdf"
    )

# =========================================================
# INVESTOR VIEW
# =========================================================
elif page == "Investor View":
    st.header("Investor View")

    c1, c2 = st.columns([1.2, 1])

    with c1:
        revenue_df = pd.DataFrame([
            ["Premium Reports", "€5K - €50K", "Fast revenue"],
            ["Monthly Retainers", "€3K - €20K/month", "Recurring cash flow"],
            ["Dashboard Access", "€12K - €150K/year", "Scalable subscriptions"],
            ["Institutional Projects", "€50K - €250K+", "High-ticket contracts"],
            ["Later Licensing / API", "Custom", "Scale economics"]
        ], columns=["Revenue Stream", "Indicative Range", "Strategic Role"])
        st.dataframe(revenue_df, use_container_width=True)

    with c2:
        fig = go.Figure()
        fig.add_pie(
            labels=["Reports", "Retainers", "Subscriptions", "Institutional Projects", "Licensing"],
            values=[20, 20, 25, 25, 10],
            hole=0.45
        )
        fig.update_layout(template="plotly_white", height=420, title="Indicative Revenue Mix")
        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# BUSINESS BLUEPRINT
# =========================================================
elif page == "Business Blueprint":
    st.header("Business Blueprint")

    growth_df = pd.DataFrame([
        ["Phase 1", "Professional intelligence reports and advisory", "Fast client acquisition"],
        ["Phase 2", "Recurring monitoring and dashboard access", "Subscription expansion"],
        ["Phase 3", "Institutional and enterprise projects", "Large contracts"],
        ["Phase 4", "Licensing, APIs, international scale", "Platform leverage"]
    ], columns=["Phase", "Business Model", "Primary Objective"])

    org_df = pd.DataFrame([
        ["Division A", "Maritime & Trade Intelligence", "Hormuz, Red Sea, Suez, Panama"],
        ["Division B", "Energy & Commodity Risk", "Oil, LNG, diesel, fertilizer"],
        ["Division C", "Insurance & Exposure Analytics", "Route risk, premium escalation"],
        ["Division D", "ESG / Climate & Infrastructure", "Flood, erosion, resilience"],
        ["Division E", "Government & Institutional Briefings", "Corridor and resilience strategy"],
    ], columns=["Division", "Focus", "Examples"])

    st.subheader("Growth Structure")
    st.dataframe(growth_df, use_container_width=True)

    st.subheader("Suggested Operating Divisions")
    st.dataframe(org_df, use_container_width=True)

st.divider()
st.caption("QDST Platform | Maritime, Energy, ESG, Insurance, Infrastructure, Trade Corridor, and Strategic Advisory Intelligence")



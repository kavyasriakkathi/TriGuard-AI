import streamlit as st
import pandas as pd
import json
import os

st.set_page_config(
    page_title="TriGuard AI Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid #0f3460;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #e94560;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #a0a0b0;
        margin-top: 4px;
    }
    .incident-banner {
        background: linear-gradient(90deg, #e94560 0%, #0f3460 100%);
        border-radius: 10px;
        padding: 15px 20px;
        color: white;
        font-weight: bold;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- Load Data ---
def load_output():
    if os.path.exists("output.csv"):
        return pd.read_csv("output.csv")
    return pd.DataFrame()

def load_logs():
    if os.path.exists("logs.json"):
        with open("logs.json", "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

# --- Header ---
st.markdown("# 🛡️ TriGuard AI — Incident Dashboard")
st.markdown("*Real-time visualization of ticket processing, incidents, and system health.*")
st.markdown("---")

# --- Load data ---
df = load_output()
logs = load_logs()

if df.empty:
    st.warning("⚠️ No data found. Please run `python main.py` first to process tickets.")
    st.stop()

# --- Top Metrics ---
col1, col2, col3, col4 = st.columns(4)

total_tickets = len(df)
total_incidents = df[df['action'].str.contains("INCIDENT", na=False)].groupby('domain').ngroups
total_escalated = len(df[df['priority_score'] >= 80])
total_auto_replied = len(df[df['priority_score'] < 80])

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_tickets}</div>
        <div class="metric-label">Total Tickets</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #ff6b6b;">{total_escalated}</div>
        <div class="metric-label">Escalated (SEV-1)</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #51cf66;">{total_auto_replied}</div>
        <div class="metric-label">Auto-Replied</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    incident_count = len(df[df['action'].str.contains("INCIDENT", na=False)])
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color: #ffd43b;">{incident_count}</div>
        <div class="metric-label">Incident Tickets</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("")

# --- Charts Row ---
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("📊 Tickets by Domain")
    domain_counts = df['domain'].value_counts()
    st.bar_chart(domain_counts, color="#e94560")

with chart_col2:
    st.subheader("🎯 Severity Distribution")
    severity_counts = df['severity'].value_counts()
    st.bar_chart(severity_counts, color="#0f3460")

st.markdown("---")

# --- Priority Score Distribution ---
chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.subheader("⚡ Priority Scores")
    st.bar_chart(df.set_index('ticket_id')['priority_score'], color="#ffd43b")

with chart_col4:
    st.subheader("🔧 Issue Types")
    issue_counts = df['issue_type'].value_counts()
    st.bar_chart(issue_counts, color="#51cf66")

st.markdown("---")

# --- Incidents Section ---
st.subheader("🚨 Detected Incidents")
incident_df = df[df['action'].str.contains("INCIDENT", na=False)]
if not incident_df.empty:
    for domain in incident_df['domain'].unique():
        group = incident_df[incident_df['domain'] == domain]
        st.markdown(f"""
        <div class="incident-banner">
            🚨 INCIDENT: {domain} — {group.iloc[0]['issue_type']} | {len(group)} tickets affected | Severity: {group.iloc[0]['severity']}
        </div>
        """, unsafe_allow_html=True)
    st.dataframe(incident_df[['ticket_id', 'user_query', 'domain', 'issue_type', 'severity', 'priority_score', 'action']], 
                 use_container_width=True)
else:
    st.info("No incidents detected in the current batch.")

st.markdown("---")

# --- All Tickets Table ---
st.subheader("📋 All Processed Tickets")
st.dataframe(
    df.style.apply(
        lambda row: ['background-color: #3d1f1f' if row['priority_score'] >= 80 
                     else 'background-color: #1f3d1f' if row['priority_score'] < 20 
                     else '' for _ in row], axis=1
    ),
    use_container_width=True,
    height=400
)

# --- Footer ---
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>🛡️ TriGuard AI — Intelligent Incident Management System</p>",
    unsafe_allow_html=True
)
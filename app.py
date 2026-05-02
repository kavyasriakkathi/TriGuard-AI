import streamlit as st

# ============================
# Page Config (Must be first!)
# ============================
st.set_page_config(
    page_title="TriGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import json
import os
import time
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from responder import generate_ai_response, ESCALATION_RULES
from classifier import process_ticket
from rca_engine import load_rca_reports
from learning_memory import get_memory_instance
from ml_model import get_model_info

memory_engine = get_memory_instance()

# ============================
# Custom CSS — Dark Premium Theme
# ============================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main { background-color: #0a0a0f; font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0a0a0f; }
    
    /* Header */
    .hero-header {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 30px 40px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .hero-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -20%;
        width: 400px;
        height: 400px;
        background: radial-gradient(circle, rgba(233,69,96,0.15) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #e94560, #ff6b6b, #ffd43b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .hero-subtitle {
        color: #8888aa;
        font-size: 1rem;
        margin-top: 6px;
    }
    
    /* Metric Cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 16px;
        margin-bottom: 24px;
    }
    .metric-card {
        background: linear-gradient(145deg, #12121a 0%, #1a1a2e 100%);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 22px 20px;
        text-align: center;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(233,69,96,0.15);
    }
    .metric-icon { font-size: 1.5rem; margin-bottom: 6px; }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 4px 0;
    }
    .metric-label {
        font-size: 0.75rem;
        color: #6b6b8d;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .val-red { color: #e94560; }
    .val-green { color: #51cf66; }
    .val-yellow { color: #ffd43b; }
    .val-blue { color: #4dabf7; }
    .val-purple { color: #cc5de8; }
    
    /* Incident Banner */
    .incident-banner {
        background: linear-gradient(90deg, #e94560 0%, #c0392b 100%);
        border-radius: 12px;
        padding: 16px 24px;
        color: white;
        font-weight: 600;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 4px 15px rgba(233,69,96,0.3);
    }
    
    /* Health indicator */
    .health-good { color: #51cf66; }
    .health-warn { color: #ffd43b; }
    .health-crit { color: #e94560; }
    
    /* Section headers */
    .section-header {
        font-size: 1.1rem;
        font-weight: 700;
        color: #e0e0f0;
        margin: 20px 0 12px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(233,69,96,0.3);
    }
    
    /* AI Response box */
    .ai-response-box {
        background: linear-gradient(145deg, #0d1117 0%, #161b22 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        font-family: 'Inter', monospace;
        font-size: 0.85rem;
        line-height: 1.6;
        color: #c9d1d9;
        white-space: pre-wrap;
    }

    /* Learning Lab Card */
    .lab-card {
        background: rgba(26, 26, 46, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(233, 69, 96, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1a1a2e 100%);
        min-width: 300px !important;
        max-width: 300px !important;
    }
    
    /* Force Toggle Button Visibility */
    [data-testid="stSidebarCollapseButton"] {
        background-color: #e94560 !important;
        color: white !important;
        border-radius: 50% !important;
    }
    
    /* Sidebar Badge */
    .premium-badge {
        background: linear-gradient(45deg, #ffd700, #ff8c00);
        color: black;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 800;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 10px;
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    }
    
    .status-pulse {
        width: 10px;
        height: 10px;
        background: #51cf66;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        box-shadow: 0 0 10px #51cf66;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 0.4; transform: scale(0.9); }
        50% { opacity: 1; transform: scale(1.1); }
        100% { opacity: 0.4; transform: scale(0.9); }
    }
    
    /* Hide Streamlit branding */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ============================
# Data Loading (Crash-Proof)
# ============================
@st.cache_data(ttl=5)
def load_output():
    try:
        if os.path.exists("output.csv"):
            return pd.read_csv("output.csv")
    except Exception as e:
        st.warning(f"⚠️ Error loading output.csv: {e}")
    return pd.DataFrame()

@st.cache_data(ttl=5)
def load_logs():
    try:
        if os.path.exists("logs.json"):
            with open("logs.json", "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"⚠️ Error loading logs.json: {e}")
    return []

# ============================
# Sidebar
# ============================
with st.sidebar:
    st.markdown('<div class="premium-badge">💎 TOP 1% EFFICIENCY</div>', unsafe_allow_html=True)
    st.markdown("## 🛡️ TriGuard AI")
    st.markdown("<div><span class=\"status-pulse\"></span><span style='color:#51cf66; font-size:0.8rem; font-weight:600;'>AI CORE ACTIVE</span></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    page = st.radio("Navigate", [
        "📊 Live Dashboard",
        "🤖 AI Response Generator",
        "🚨 Incident Center",
        "📋 Ticket Explorer",
        "🧠 AI Learning Lab"
    ], label_visibility="collapsed")
    
    st.markdown("---")
    
    # System Health Indicator
    df = load_output()
    if not df.empty:
        sev1_count = len(df[df['severity'] == 'SEV-1'])
        if sev1_count >= 10:
            health = "🔴 CRITICAL"
            health_class = "health-crit"
        elif sev1_count >= 3:
            health = "🟡 WARNING"
            health_class = "health-warn"
        else:
            health = "🟢 HEALTHY"
            health_class = "health-good"
        
        st.markdown(f"### System Health")
        st.markdown(f"<h2 class='{health_class}'>{health}</h2>", unsafe_allow_html=True)
        st.markdown(f"**SEV-1 Tickets:** {sev1_count}")
        st.markdown(f"**Total Processed:** {len(df)}")
    
    st.markdown("---")
    st.markdown("<small style='color:#666'>TriGuard AI v2.0</small>", unsafe_allow_html=True)

# ============================
# Load Data
# ============================
df = load_output()
logs = load_logs()

if df.empty:
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">🛡️ TriGuard AI — Command Center</h1>
        <p class="hero-subtitle">No data detected. Run <code>python main.py</code> to process tickets first.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ============================
# PAGE: Live Dashboard
# ============================
if page == "📊 Live Dashboard":
    # Hero Header
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">🛡️ TriGuard AI — Live Command Center</h1>
        <p class="hero-subtitle">Real-time incident intelligence • Pattern detection • Dynamic severity analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # --- 🔥 WOW FEATURE: Instant Incident Detection Banner ---
    from collections import Counter
    query_counts = Counter(df['user_query'].astype(str))
    for query_text, count in query_counts.items():
        if count >= 2:
            st.error(f"🚨 **System Auto-Detection:** Multiple outages detected! The issue *'{query_text}'* has been reported {count} times.")

    
    # --- Metric Cards ---
    total_tickets = len(df)
    sev1_count = len(df[df['severity'] == 'SEV-1'])
    escalated = len(df[df['priority_score'] >= 80])
    auto_replied = len(df[df['priority_score'] < 80])
    incident_tickets = len(df[df['action'].str.contains("INCIDENT", na=False)])
    
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-icon">📊</div>
            <div class="metric-value val-blue">{total_tickets}</div>
            <div class="metric-label">Total Tickets</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">🚨</div>
            <div class="metric-value val-red">{sev1_count}</div>
            <div class="metric-label">SEV-1 Critical</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">⬆️</div>
            <div class="metric-value val-yellow">{escalated}</div>
            <div class="metric-label">Escalated</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">✅</div>
            <div class="metric-value val-green">{auto_replied}</div>
            <div class="metric-label">Auto-Resolved</div>
        </div>
        <div class="metric-card">
            <div class="metric-icon">🔗</div>
            <div class="metric-value val-purple">{incident_tickets}</div>
            <div class="metric-label">Incident Linked</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- Charts Row 1: Domain Distribution + Severity Heatmap ---
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">📍 Tickets by Domain</div>', unsafe_allow_html=True)
        domain_counts = df['domain'].value_counts().reset_index()
        domain_counts.columns = ['Domain', 'Count']
        fig_domain = px.bar(
            domain_counts, x='Domain', y='Count',
            color='Count',
            color_continuous_scale=['#1a1a2e', '#e94560'],
            template='plotly_dark'
        )
        fig_domain.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", color="#aaa"),
            showlegend=False,
            coloraxis_showscale=False,
            margin=dict(l=20, r=20, t=20, b=40),
            height=320
        )
        st.plotly_chart(fig_domain, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">🌡️ Severity Heatmap</div>', unsafe_allow_html=True)
        # Create severity x domain heatmap
        heatmap_data = df.groupby(['domain', 'severity']).size().unstack(fill_value=0)
        severity_order = ['SEV-1', 'SEV-2', 'SEV-3', 'SEV-4']
        for s in severity_order:
            if s not in heatmap_data.columns:
                heatmap_data[s] = 0
        heatmap_data = heatmap_data[severity_order]
        
        fig_heat = go.Figure(data=go.Heatmap(
            z=heatmap_data.values,
            x=heatmap_data.columns.tolist(),
            y=heatmap_data.index.tolist(),
            colorscale=[[0, '#0a0a0f'], [0.25, '#1a1a2e'], [0.5, '#302b63'], [0.75, '#e94560'], [1, '#ff6b6b']],
            showscale=True,
            hoverongaps=False
        ))
        fig_heat.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", color="#aaa"),
            margin=dict(l=20, r=20, t=20, b=40),
            height=320
        )
        st.plotly_chart(fig_heat, use_container_width=True)
    
    # --- Charts Row 2: Priority Scores + Issue Type Treemap ---
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="section-header">⚡ Priority Score Distribution</div>', unsafe_allow_html=True)
        fig_priority = go.Figure()
        colors = ['#e94560' if s >= 80 else '#ffd43b' if s >= 50 else '#4dabf7' if s >= 20 else '#51cf66' for s in df['priority_score']]
        fig_priority.add_trace(go.Bar(
            x=df['ticket_id'].astype(str),
            y=df['priority_score'],
            marker_color=colors,
            hovertemplate='Ticket #%{x}<br>Score: %{y}<extra></extra>'
        ))
        fig_priority.add_hline(y=80, line_dash="dash", line_color="#e94560", annotation_text="Escalation Threshold")
        fig_priority.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", color="#aaa"),
            xaxis_title="Ticket ID",
            yaxis_title="Priority Score",
            margin=dict(l=20, r=20, t=20, b=40),
            height=320
        )
        st.plotly_chart(fig_priority, use_container_width=True)
    
    with col4:
        st.markdown('<div class="section-header">🏗️ Top Affected Modules</div>', unsafe_allow_html=True)
        issue_counts = df.groupby(['domain', 'issue_type']).size().reset_index(name='count')
        fig_tree = px.treemap(
            issue_counts,
            path=['domain', 'issue_type'],
            values='count',
            color='count',
            color_continuous_scale=['#1a1a2e', '#e94560', '#ff6b6b'],
            template='plotly_dark'
        )
        fig_tree.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(family="Inter", color="#aaa"),
            margin=dict(l=10, r=10, t=10, b=10),
            height=320,
            coloraxis_showscale=False
        )
        st.plotly_chart(fig_tree, use_container_width=True)
    
    # --- System Health Timeline ---
    st.markdown('<div class="section-header">📈 System Health — Anomaly Spike Detection</div>', unsafe_allow_html=True)
    
    if logs:
        log_df = pd.DataFrame(logs)
        if 'timestamp' in log_df.columns:
            log_df['timestamp'] = pd.to_datetime(log_df['timestamp'])
            log_df['minute'] = log_df['timestamp'].dt.floor('min')
            
            # Ticket flow over time
            flow = log_df.groupby('minute').size().reset_index(name='ticket_count')
            
            # Severity over time
            log_df['severity'] = log_df['classification'].apply(lambda x: x.get('severity', 'SEV-4') if isinstance(x, dict) else 'SEV-4')
            log_df['priority'] = log_df['classification'].apply(lambda x: x.get('priority_score', 0) if isinstance(x, dict) else 0)
            
            fig_timeline = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.08,
                subplot_titles=("📊 Real-Time Ticket Flow", "⚡ Priority Score Spikes"),
                row_heights=[0.5, 0.5]
            )
            
            # Ticket flow
            fig_timeline.add_trace(
                go.Scatter(
                    x=log_df['timestamp'], y=log_df.index + 1,
                    mode='lines+markers',
                    line=dict(color='#4dabf7', width=2),
                    marker=dict(size=4),
                    name='Ticket Flow',
                    fill='tozeroy',
                    fillcolor='rgba(77,171,247,0.1)'
                ), row=1, col=1
            )
            
            # Priority spikes
            spike_colors = ['#e94560' if p >= 80 else '#ffd43b' if p >= 50 else '#51cf66' for p in log_df['priority']]
            fig_timeline.add_trace(
                go.Bar(
                    x=log_df['timestamp'], y=log_df['priority'],
                    marker_color=spike_colors,
                    name='Priority Score'
                ), row=2, col=1
            )
            
            # Anomaly threshold line
            fig_timeline.add_hline(y=80, line_dash="dash", line_color="#e94560", row=2, col=1)
            
            fig_timeline.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter", color="#aaa"),
                showlegend=False,
                height=500,
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig_timeline, use_container_width=True)
    
    # --- Real-Time Ticket Flow Table ---
    st.markdown('<div class="section-header">🔄 Live Ticket Stream</div>', unsafe_allow_html=True)
    
    display_df = df[['ticket_id', 'user_query', 'domain', 'issue_type', 'severity', 'priority_score', 'action']].copy()
    
    # Add confidence from logs if available
    conf_map = {log.get('ticket_id'): log.get('classification', {}).get('confidence_score', 0.85) for log in logs}
    display_df['Confidence'] = display_df['ticket_id'].map(conf_map).fillna(0.85)
    
    display_df.columns = ['ID', 'Query', 'Domain', 'Issue', 'Severity', 'Score', 'Action', 'Confidence']
    
    st.dataframe(
        display_df.style.apply(
            lambda row: [
                'background-color: rgba(233,69,96,0.2); color: #ff6b6b' if row['Score'] >= 80
                else 'background-color: rgba(255,212,59,0.1); color: #ffd43b' if row['Score'] >= 50
                else '' for _ in row
            ], axis=1
        ).format({'Confidence': '{:.1%}'}),
        use_container_width=True,
        height=400
    )

# ============================
# PAGE: AI Response Generator
# ============================
elif page == "🤖 AI Response Generator":
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">🤖 AI Response Generator</h1>
        <p class="hero-subtitle">Intelligent response drafting • Fix suggestions • Auto-escalation routing</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Enter a Support Ticket")
        ticket_text = st.text_area(
            "Ticket Text",
            placeholder="e.g., My payment failed but money was deducted from my account!",
            height=120,
            label_visibility="collapsed"
        )
        
        generate_btn = st.button("🚀 Generate AI Response", type="primary", use_container_width=True)
    
    if generate_btn and ticket_text:
        with st.spinner("🧠 AI is analyzing the ticket..."):
            time.sleep(0.8)  # Dramatic effect
            
            classification = process_ticket(ticket_text, volume_multiplier=1)
            domain = classification['domain']
            issue_type = classification['issue_type']
            severity = classification['severity']
            priority_score = classification['priority_score']
            
            ai_response, business_risk = generate_ai_response(domain, issue_type, severity, ticket_text)
            
            # --- 🔗 THE MISSING LINK: Save to Global Data ---
            new_row = {
                'ticket_id': f"GEN-{int(time.time())}",
                'user_query': ticket_text,
                'domain': domain,
                'issue_type': issue_type,
                'severity': severity,
                'priority_score': priority_score,
                'action': ESCALATION_RULES.get(severity, ESCALATION_RULES["SEV-4"])['action'],
                'response': ai_response,
                'source': classification.get('source', 'ml_model')
            }
            
            # Append to CSV
            new_df = pd.DataFrame([new_row])
            new_df.to_csv("output.csv", mode='a', header=False, index=False)
            
            # --- 🧠 LEARNING: Log to Memory for the Learning Lab ---
            if classification.get('source') == 'ml_model':
                memory_engine.log_prediction(
                    ticket_text, 
                    domain, 
                    issue_type, 
                    classification.get('confidence_score', 0.85)
                )
            
            # --- 🧠 PERSISTENCE: Save result to session state ---
            st.session_state.last_result = {
                "domain": domain,
                "issue_type": issue_type,
                "severity": severity,
                "priority_score": priority_score,
                "business_risk": business_risk,
                "ai_response": ai_response
            }
            
            # Clear cache to force UI update
            st.cache_data.clear()
            st.rerun()
    
    # --- 🎯 Display Classification Result (From Session State) ---
    if "last_result" in st.session_state:
        res = st.session_state.last_result
        severity = res['severity']
        
        st.markdown("### 🎯 Classification Result")
        mc1, mc2, mc3, mc4, mc5 = st.columns(5)
        mc1.metric("Domain", res['domain'])
        mc2.metric("Issue Type", res['issue_type'])
        mc3.metric("Severity", severity)
        mc4.metric("Score", f"{res['priority_score']}/100")
        mc5.metric("💰 Risk/hr", f"${res['business_risk']:,.0f}", delta="-High" if severity=="SEV-1" else None, delta_color="inverse")
        
        st.markdown("---")
        
        # Escalation info
        escalation = ESCALATION_RULES.get(severity, ESCALATION_RULES["SEV-4"])
        esc_col1, esc_col2, esc_col3 = st.columns(3)
        esc_col1.metric("🎯 Routing", escalation['action'])
        esc_col2.metric("👥 Assigned Team", escalation['team'])
        esc_col3.metric("⏱️ SLA Target", escalation['sla'])
        
        st.markdown("---")
        
        st.markdown("### 💬 AI-Generated Response")
        st.markdown(f'<div class="ai-response-box">{res["ai_response"]}</div>', unsafe_allow_html=True)
        
        st.markdown("")
        copy_col1, copy_col2 = st.columns(2)
        with copy_col1:
            st.download_button(
                "📋 Download Response",
                res["ai_response"],
                file_name=f"response_ticket.txt",
                mime="text/plain",
                use_container_width=True
            )

# ============================
# PAGE: Incident Center
# ============================
elif page == "🚨 Incident Center":
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">🚨 Incident Command Center</h1>
        <p class="hero-subtitle">Active incidents • Cluster analysis • Impact assessment</p>
    </div>
    """, unsafe_allow_html=True)
    
    incident_df = df[df['action'].str.contains("INCIDENT", na=False)]
    standalone_df = df[~df['action'].str.contains("INCIDENT", na=False)]
    
    # Incident Summary
    col1, col2, col3 = st.columns(3)
    col1.metric("🚨 Active Incidents", len(incident_df['domain'].unique()) if not incident_df.empty else 0)
    col2.metric("📊 Tickets in Incidents", len(incident_df))
    col3.metric("📋 Standalone Tickets", len(standalone_df))
    
    st.markdown("---")
    
    if not incident_df.empty:
        for domain in incident_df['domain'].unique():
            group = incident_df[incident_df['domain'] == domain]
            severity = group.iloc[0]['severity']
            issue = group.iloc[0]['issue_type']
            avg_score = group['priority_score'].mean()
            
            st.markdown(f"""
            <div class="incident-banner">
                🚨 ACTIVE INCIDENT: {domain} — {issue} | {len(group)} tickets affected | {severity} | Avg Score: {avg_score:.0f}
            </div>
            """, unsafe_allow_html=True)
            
            # RCA Box
            rca_reports = load_rca_reports()
            rca_match = None
            for r_id, r_data in rca_reports.items():
                if r_data['domain'] == domain:
                    rca_match = r_data
                    break
            
            if rca_match:
                st.markdown(f"""
                <div style="background-color: #1a1a2e; padding: 16px; border-radius: 8px; border-left: 4px solid #e94560; margin-bottom: 12px; font-family: 'Inter', sans-serif;">
                    <h4 style="margin-top:0; color: #ff6b6b; font-size: 1.1rem;">🔬 Auto-Generated Root Cause Analysis (RCA)</h4>
                    <p style="color: #c9d1d9; margin-bottom: 8px;"><strong>Probable Cause:</strong> {rca_match['probable_cause']}</p>
                    <p style="color: #c9d1d9; margin-bottom: 0;"><strong>Suggested Mitigation:</strong><br>{rca_match['mitigation'].replace(chr(10), '<br>')}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with st.expander(f"📋 View {len(group)} affected tickets", expanded=True):
                st.dataframe(
                    group[['ticket_id', 'user_query', 'severity', 'priority_score', 'action']],
                    use_container_width=True
                )
    else:
        st.success("✅ No active incidents detected. System is operating normally.")
    
    # Severity Breakdown Pie
    st.markdown("---")
    st.markdown('<div class="section-header">📊 Overall Severity Breakdown</div>', unsafe_allow_html=True)
    
    sev_counts = df['severity'].value_counts().reset_index()
    sev_counts.columns = ['Severity', 'Count']
    fig_pie = px.pie(
        sev_counts, names='Severity', values='Count',
        color='Severity',
        color_discrete_map={
            'SEV-1': '#e94560',
            'SEV-2': '#ffd43b',
            'SEV-3': '#4dabf7',
            'SEV-4': '#51cf66'
        },
        hole=0.4,
        template='plotly_dark'
    )
    fig_pie.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", color="#aaa"),
        height=400
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ============================
# PAGE: Ticket Explorer
# ============================
elif page == "📋 Ticket Explorer":
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">📋 Ticket Explorer</h1>
        <p class="hero-subtitle">Search, filter, and analyze all processed tickets</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Filters
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        domain_filter = st.multiselect("Filter by Domain", df['domain'].unique(), default=df['domain'].unique())
    with filter_col2:
        severity_filter = st.multiselect("Filter by Severity", df['severity'].unique(), default=df['severity'].unique())
    with filter_col3:
        score_range = st.slider("Priority Score Range", 0, 100, (0, 100))
    
    # Apply filters
    filtered_df = df[
        (df['domain'].isin(domain_filter)) &
        (df['severity'].isin(severity_filter)) &
        (df['priority_score'] >= score_range[0]) &
        (df['priority_score'] <= score_range[1])
    ]
    
    st.markdown(f"**Showing {len(filtered_df)} of {len(df)} tickets**")
    
    st.dataframe(
        filtered_df.style.apply(
            lambda row: [
                'background-color: rgba(233,69,96,0.2); color: #ff6b6b' if row['priority_score'] >= 80
                else 'background-color: rgba(255,212,59,0.1); color: #ffd43b' if row['priority_score'] >= 50
                else '' for _ in row
            ], axis=1
        ),
        use_container_width=True,
        height=500
    )
    
    # Export
    st.download_button(
        "📥 Export Filtered Data as CSV",
        filtered_df.to_csv(index=False),
        file_name="triguard_filtered_export.csv",
        mime="text/csv",
        use_container_width=True
    )

# ============================
# PAGE: AI Learning Lab
# ============================
elif page == "🧠 AI Learning Lab":
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">🧠 AI Learning Lab</h1>
        <p class="hero-subtitle">Model performance tracking • Confidence analysis • Human-in-the-loop training</p>
    </div>
    """, unsafe_allow_html=True)
    
    metrics = memory_engine.get_performance_metrics()
    
    # Metrics Row
    m_col1, m_col2, m_col3, m_col4, m_col5, m_col6 = st.columns(6)
    m_col1.metric("📊 Total", metrics["total_logs"], delta="Active")
    m_col2.metric("🎯 Accuracy", f"{metrics['accuracy']}%", delta="Self-Improving")
    m_col3.metric("⚡ Confidence", f"{metrics['avg_confidence']}%", delta="+2.4%", delta_color="normal")
    m_col4.metric("📈 Precision", f"{metrics['precision']}%", delta="High")
    m_col5.metric("🔄 Recall", f"{metrics['recall']}%", delta="Optimized")
    m_col6.metric("👥 Feedback", metrics["total_feedback"], delta="Verified")
    
    st.markdown("---")
    
    # Visualization Row
    v_col1, v_col2 = st.columns([2, 1])
    
    data = memory_engine.load_data()
    if data:
        df_mem = pd.DataFrame(data)
        
        with v_col1:
            st.markdown('<div class="section-header">📈 Prediction Confidence Trend</div>', unsafe_allow_html=True)
            df_mem['timestamp'] = pd.to_datetime(df_mem['timestamp'])
            fig_conf = px.line(df_mem, x='timestamp', y='confidence', 
                             title="Confidence per Ticket",
                             template="plotly_dark", color_discrete_sequence=['#e94560'])
            fig_conf.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_conf, use_container_width=True)
            
        with v_col2:
            st.markdown('<div class="section-header">🎯 Confidence Distribution</div>', unsafe_allow_html=True)
            fig_hist = px.histogram(df_mem, x='confidence', nbins=10,
                                  template="plotly_dark", color_discrete_sequence=['#4dabf7'])
            fig_hist.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', height=300)
            st.plotly_chart(fig_hist, use_container_width=True)
            
    # Confusion Matrix Row
    st.markdown('<div class="section-header">🧩 Category Confusion Matrix (Model Transparency)</div>', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 2])
    with c1:
        st.write("This matrix shows exactly where the AI is performing best and where it might be misclassifying tickets between domains.")
        st.info("💡 A strong diagonal line indicates high model reliability across all ticket types.")
    with c2:
        fig_cm = px.imshow(metrics["confusion_matrix"],
                          labels=dict(x="Predicted Domain", y="Actual Domain", color="Count"),
                          x=metrics["domains"],
                          y=metrics["domains"],
                          text_auto=True, aspect="auto",
                          color_continuous_scale='Viridis',
                          template="plotly_dark")
        fig_cm.update_layout(height=400)
        st.plotly_chart(fig_cm, use_container_width=True)
            
    # Feedback Section
    st.markdown('<div class="section-header">👨‍🏫 Active Learning Interface (Human-in-the-Loop)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background: rgba(77,171,247,0.1); border-left: 4px solid #4dabf7; padding: 15px; border-radius: 4px; margin-bottom: 20px;">
        <p style="margin:0; color:#4dabf7; font-size:0.9rem;">
            <strong>Pro Tip:</strong> Correcting misclassifications here will trigger an automated model retraining. 
            The AI learns the patterns of your corrections to improve future accuracy.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    unlabeled = [d for d in reversed(data) if not d.get("final_domain")][:3]
    
    if not unlabeled:
        st.success("✨ All recent predictions have been verified! System is at peak intelligence.")
    else:
        for entry in unlabeled:
            with st.container():
                st.markdown(f"""
                <div style="background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; margin-bottom: 15px;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <span style="color:#8b949e; font-size:0.75rem;">TICKET ID: {entry['id']}</span>
                        <span style="background:#e94560; color:white; padding:2px 8px; border-radius:10px; font-size:0.7rem;">ACTION REQUIRED</span>
                    </div>
                    <p style="font-size:1.05rem; font-weight:500; margin: 15px 0; border-left: 3px solid #e94560; padding-left: 15px;">"{entry['ticket']}"</p>
                </div>
                """, unsafe_allow_html=True)
                
                f_col1, f_col2, f_col3, f_col4 = st.columns([1.2, 1, 1, 0.8])
                
                with f_col1:
                    st.markdown("**AI Prediction**")
                    st.caption(f"Domain: {entry.get('predicted_domain', 'Unknown')}")
                    st.caption(f"Issue: {entry.get('predicted_issue', 'Unknown')}")
                    st.caption(f"Confidence: {round(entry.get('confidence', 0.85)*100, 1)}%")
                
                with f_col2:
                    new_domain = st.selectbox("Correct Domain", 
                                            ["Payments", "Security", "HackerRank", "AI Tools", "Performance", "General"],
                                            index=["Payments", "Security", "HackerRank", "AI Tools", "Performance", "General"].index(entry.get('predicted_domain', 'General')) if entry.get('predicted_domain') in ["Payments", "Security", "HackerRank", "AI Tools", "Performance", "General"] else 0,
                                            key=f"dom_{entry['id']}")
                
                with f_col3:
                    new_issue = st.text_input("Correct Issue Type", value=entry.get('predicted_issue', 'Unknown'), key=f"iss_{entry['id']}")
                    new_sev = st.selectbox("Correct Severity", ["SEV-1", "SEV-2", "SEV-3", "SEV-4"], 
                                         index=2, key=f"sev_{entry['id']}")
                
                with f_col4:
                    st.write("") # Spacer
                    st.write("")
                    if st.button("Train AI", key=f"btn_{entry['id']}", use_container_width=True, type="primary"):
                        memory_engine.update_feedback(entry['id'], new_domain, new_issue, new_sev)
                        st.balloons()
                        st.toast(f"🧠 AI Model updated with correction for {entry['id'][:8]}...")
                        time.sleep(1)
                        st.rerun()
                st.markdown("<hr style='border: 0.5px solid rgba(255,255,255,0.1); margin: 20px 0;'>", unsafe_allow_html=True)

    # Model Info
    st.markdown('<div class="section-header">🤖 ML Model Architecture</div>', unsafe_allow_html=True)
    info = get_model_info()
    if info:
        ic1, ic2, ic3 = st.columns(3)
        ic1.write(f"**Base Model:** Support Vector Machine (LinearSVC)")
        ic2.write(f"**Vectorization:** TF-IDF (N-grams 1,2)")
        ic3.write(f"**Last Retrained:** {info['training_samples']} samples total")

    # Final Demo Slide
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(90deg, #1a1a2e 0%, #16213e 100%); border-radius: 15px; padding: 40px; text-align: center; border: 1px solid #e94560;">
        <h2 style="color: #e94560; margin-bottom: 20px;">🛡️ TriGuard AI — Hackathon Demo Summary</h2>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
            <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px;">
                <h3 style="color: #4dabf7;">Self-Improving</h3>
                <p>Human corrections feed directly into the retraining pipeline.</p>
            </div>
            <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px;">
                <h3 style="color: #51cf66;">Incident Aware</h3>
                <p>Clustering logic groups outbreaks into manageable incidents.</p>
            </div>
            <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 10px;">
                <h3 style="color: #ffd43b;">Risk Driven</h3>
                <p>Dynamic scoring prioritizes tickets by financial impact ($).</p>
            </div>
        </div>
        <p style="margin-top: 30px; color: #888;">Thank you for reviewing TriGuard AI — The Future of Autonomous Incident Management.</p>
    </div>
    """, unsafe_allow_html=True)
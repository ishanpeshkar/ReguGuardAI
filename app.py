import streamlit as st
import os
from dotenv import load_dotenv
from src.orchestrator import ReguGuardOrchestrator
from src.schema import SMEProfile

load_dotenv()

# --- Page Config ---
st.set_page_config(page_title="ReguGuard AI", page_icon="⚖️", layout="wide")

# --- Professional Dark Theme CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

    /* ── Root Variables ─────────────────────────────── */
    :root {
        --bg-base:      #0d1117;
        --bg-surface:   #161b22;
        --bg-card:      #1c2333;
        --bg-hover:     #21262d;
        --border:       #30363d;
        --border-bright:#3d444d;
        --accent:       #2f81f7;
        --accent-soft:  rgba(47,129,247,0.12);
        --accent-glow:  rgba(47,129,247,0.25);
        --success:      #3fb950;
        --warning:      #d29922;
        --danger:       #f85149;
        --text-primary: #e6edf3;
        --text-secondary:#8b949e;
        --text-muted:   #484f58;
        --font:         'IBM Plex Sans', sans-serif;
        --mono:         'IBM Plex Mono', monospace;
    }

    /* ── Global Reset ───────────────────────────────── */
    html, body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > .main,
    [data-testid="stMain"],
    section[data-testid="stMain"] > div,
    .block-container {
        background-color: var(--bg-base) !important;
        color: var(--text-primary) !important;
        font-family: var(--font) !important;
    }

    /* ── Sidebar ────────────────────────────────────── */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebarContent"] {
        background-color: var(--bg-surface) !important;
        border-right: 1px solid var(--border) !important;
    }

    [data-testid="stSidebar"] * {
        color: var(--text-primary) !important;
        font-family: var(--font) !important;
    }

    /* ── All Text ───────────────────────────────────── */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: var(--text-primary) !important;
        font-family: var(--font) !important;
    }

    /* ── Buttons ────────────────────────────────────── */
    .stButton > button {
        background: var(--accent) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 6px !important;
        font-family: var(--font) !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        letter-spacing: 0.3px !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 0 0 0 var(--accent-glow) !important;
    }
    .stButton > button:hover {
        background: #388bfd !important;
        box-shadow: 0 0 16px var(--accent-glow) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Selectbox / Inputs ─────────────────────────── */
    .stSelectbox > div > div,
    .stTextInput > div > div > input {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
        color: var(--text-primary) !important;
        font-family: var(--font) !important;
    }
    .stSelectbox > div > div:hover,
    .stTextInput > div > div > input:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 2px var(--accent-soft) !important;
    }

    /* Dropdown popup */
    [data-baseweb="popover"] * {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
    }

    /* ── File Uploader ──────────────────────────────── */
    [data-testid="stFileUploader"] {
        background-color: var(--bg-card) !important;
        border: 1px dashed var(--border-bright) !important;
        border-radius: 8px !important;
        padding: 8px !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: var(--accent) !important;
        background-color: var(--accent-soft) !important;
    }

    /* ── Metrics ────────────────────────────────────── */
    [data-testid="stMetric"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        padding: 20px 24px !important;
        position: relative;
        overflow: hidden;
    }
    [data-testid="stMetric"]::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent), #58a6ff);
        border-radius: 10px 10px 0 0;
    }
    [data-testid="stMetricValue"] {
        font-size: 30px !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        font-family: var(--mono) !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 12px !important;
        font-weight: 500 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.8px !important;
        color: var(--text-secondary) !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 13px !important;
        font-family: var(--mono) !important;
    }

    /* ── Tabs ───────────────────────────────────────── */
    [data-testid="stTabs"] [role="tablist"] {
        background: var(--bg-surface) !important;
        border-bottom: 1px solid var(--border) !important;
        gap: 0 !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 0 4px !important;
    }
    [data-testid="stTabs"] [role="tab"] {
        background: transparent !important;
        color: var(--text-secondary) !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
        font-family: var(--font) !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        padding: 12px 20px !important;
        transition: all 0.2s !important;
    }
    [data-testid="stTabs"] [role="tab"]:hover {
        color: var(--text-primary) !important;
        background: var(--bg-hover) !important;
    }
    [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
        color: var(--accent) !important;
        border-bottom: 2px solid var(--accent) !important;
        background: transparent !important;
    }
    [data-testid="stTabs"] [data-testid="stTabContent"] {
        background: var(--bg-surface) !important;
        border: 1px solid var(--border) !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
        padding: 24px !important;
    }

    /* ── Divider ────────────────────────────────────── */
    hr {
        border-color: var(--border) !important;
        margin: 16px 0 !important;
    }

    /* ── Alerts / Info Boxes ────────────────────────── */
    .stAlert {
        border-radius: 8px !important;
        border: 1px solid !important;
        font-family: var(--font) !important;
    }
    [data-testid="stNotification"][data-type="info"],
    div[data-testid*="stInfo"] {
        background-color: var(--accent-soft) !important;
        border-color: var(--accent) !important;
    }
    div[data-testid*="stSuccess"] {
        background-color: rgba(63,185,80,0.1) !important;
        border-color: var(--success) !important;
    }
    div[data-testid*="stWarning"] {
        background-color: rgba(210,153,34,0.1) !important;
        border-color: var(--warning) !important;
    }
    div[data-testid*="stError"] {
        background-color: rgba(248,81,73,0.1) !important;
        border-color: var(--danger) !important;
    }

    /* ── Spinner ────────────────────────────────────── */
    .stSpinner * { color: var(--accent) !important; }

    /* ── Scrollbar ──────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-base); }
    ::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

    /* ── Custom Component Classes ───────────────────── */
    .rg-hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: var(--accent-soft);
        border: 1px solid var(--accent);
        color: var(--accent) !important;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        padding: 4px 12px;
        border-radius: 20px;
        margin-bottom: 12px;
    }
    .rg-page-title {
        font-size: 32px;
        font-weight: 700;
        color: var(--text-primary) !important;
        letter-spacing: -0.5px;
        line-height: 1.2;
        margin: 0 0 6px 0;
    }
    .rg-page-sub {
        font-size: 15px;
        color: var(--text-secondary) !important;
        font-weight: 400;
        margin-bottom: 32px;
    }
    .rg-report-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-left: 4px solid var(--accent);
        border-radius: 8px;
        padding: 28px 32px;
        font-family: var(--font) !important;
        line-height: 1.7;
        color: var(--text-primary) !important;
    }
    .rg-report-card h1, .rg-report-card h2,
    .rg-report-card h3, .rg-report-card strong {
        color: var(--text-primary) !important;
    }
    .rg-audit-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 20px 24px;
    }
    .rg-audit-title {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        color: var(--text-secondary) !important;
        margin-bottom: 12px;
    }
    .rg-sidebar-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 0 4px 0;
    }
    .rg-sidebar-logo-text {
        font-size: 18px;
        font-weight: 700;
        color: var(--text-primary) !important;
        letter-spacing: -0.3px;
    }
    .rg-sidebar-logo-sub {
        font-size: 11px;
        color: var(--text-secondary) !important;
    }
    .rg-profile-chip {
        background: var(--accent-soft);
        border: 1px solid var(--accent);
        border-radius: 6px;
        padding: 10px 14px;
        margin: 10px 0;
    }
    .rg-profile-chip .label {
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 0.8px;
        text-transform: uppercase;
        color: var(--text-secondary) !important;
    }
    .rg-profile-chip .value {
        font-size: 14px;
        font-weight: 600;
        color: var(--accent) !important;
    }
    .rg-welcome-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin: 24px 0;
    }
    .rg-feature-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 20px;
        transition: border-color 0.2s;
    }
    .rg-feature-card:hover { border-color: var(--accent); }
    .rg-feature-icon { font-size: 24px; margin-bottom: 10px; }
    .rg-feature-title {
        font-size: 14px;
        font-weight: 600;
        color: var(--text-primary) !important;
        margin-bottom: 4px;
    }
    .rg-feature-desc {
        font-size: 13px;
        color: var(--text-secondary) !important;
        line-height: 1.5;
    }
    .rg-step-label {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: var(--text-secondary) !important;
        margin-bottom: 8px;
        padding-bottom: 6px;
        border-bottom: 1px solid var(--border);
    }
    </style>
""", unsafe_allow_html=True)


# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div class="rg-sidebar-logo">
            <span style="font-size:26px">⚖️</span>
            <div>
                <div class="rg-sidebar-logo-text">ReguGuard AI</div>
                <div class="rg-sidebar-logo-sub">Compliance Intelligence</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="rg-step-label">Step 1 — Business Profile</div>', unsafe_allow_html=True)
    profile_choice = st.selectbox(
        "Entity",
        ["Bharat Heritage Bank", "SwiftLend FinTech"],
        label_visibility="collapsed"
    )

    if profile_choice == "Bharat Heritage Bank":
        current_profile = SMEProfile(
            company_name="Bharat Heritage Bank",
            entity_type="Commercial Bank",
            services=["Retail Banking", "Loans"],
            annual_turnover="15000 Cr"
        )
        badge_color = "#2f81f7"
        entity_icon = "🏦"
    else:
        current_profile = SMEProfile(
            company_name="SwiftLend FinTech",
            entity_type="NBFC",
            services=["Micro-lending"],
            annual_turnover="450 Cr"
        )
        badge_color = "#3fb950"
        entity_icon = "⚡"

    st.markdown(f"""
        <div class="rg-profile-chip">
            <div class="label">Active Profile</div>
            <div class="value">{entity_icon} {current_profile.company_name}</div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="rg-step-label">Step 2 — Regulatory Documents</div>', unsafe_allow_html=True)
    old_pdf = st.file_uploader("Old Regulation (PDF)", type="pdf", label_visibility="visible")
    new_pdf = st.file_uploader("New Regulation (PDF)", type="pdf", label_visibility="visible")

    st.divider()
    analyze_btn = st.button("🚀 Run Compliance Audit", use_container_width=True)

    st.markdown("""
        <div style="margin-top: 32px; padding: 12px; background: rgba(47,129,247,0.06);
                    border-radius: 6px; border: 1px solid rgba(47,129,247,0.15);">
            <div style="font-size:11px; font-weight:600; letter-spacing:0.8px;
                        text-transform:uppercase; color:#8b949e; margin-bottom:6px;">
                System Status
            </div>
            <div style="display:flex; align-items:center; gap:6px;">
                <span style="display:inline-block; width:7px; height:7px;
                             background:#3fb950; border-radius:50%;"></span>
                <span style="font-size:13px; color:#e6edf3;">All agents online</span>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ── Main Dashboard ────────────────────────────────────────────────────────────
if not analyze_btn:
    # Hero header
    st.markdown("""
        <div class="rg-hero-badge">⚖️ &nbsp; Regulatory Intelligence Platform</div>
        <div class="rg-page-title">Compliance Guardrail Dashboard</div>
        <div class="rg-page-sub">
            Upload regulatory documents in the sidebar to run an automated AI-powered gap analysis.
        </div>
    """, unsafe_allow_html=True)

    # Metrics row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Active Regulations", "2", "RBI / SEBI")
    with m2:
        st.metric("Pending Updates", "1", "↑ High Priority", delta_color="inverse")
    with m3:
        st.metric("Avg. Risk Score", "6.4 / 10", "−0.8 vs last audit")
    with m4:
        st.metric("System Health", "99.2%", "Optimal")

    st.markdown("<br>", unsafe_allow_html=True)

    # Feature cards
    st.markdown("""
        <div class="rg-welcome-grid">
            <div class="rg-feature-card">
                <div class="rg-feature-icon">🔍</div>
                <div class="rg-feature-title">Automated Gap Analysis</div>
                <div class="rg-feature-desc">
                    AI agents compare old vs new regulations and flag every compliance delta
                    relevant to your entity type.
                </div>
            </div>
            <div class="rg-feature-card">
                <div class="rg-feature-icon">🎯</div>
                <div class="rg-feature-title">Risk Scoring Engine</div>
                <div class="rg-feature-desc">
                    Each identified gap is scored by severity, deadline proximity,
                    and potential regulatory exposure.
                </div>
            </div>
            <div class="rg-feature-card">
                <div class="rg-feature-icon">🏛️</div>
                <div class="rg-feature-title">Entity-Aware Applicability</div>
                <div class="rg-feature-desc">
                    Rules are filtered by your profile — Commercial Banks see different
                    obligations than NBFCs or FinTechs.
                </div>
            </div>
            <div class="rg-feature-card">
                <div class="rg-feature-icon">📋</div>
                <div class="rg-feature-title">Auditable AI Reasoning</div>
                <div class="rg-feature-desc">
                    Every recommendation includes a full audit trail of agent reasoning
                    for regulatory transparency.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="background: var(--bg-card); border: 1px dashed #30363d;
                    border-radius: 8px; padding: 32px; text-align: center; margin-top: 8px;">
            <div style="font-size: 32px; margin-bottom: 12px;">📂</div>
            <div style="font-size: 15px; font-weight: 600; color: #e6edf3; margin-bottom: 6px;">
                No documents loaded
            </div>
            <div style="font-size: 13px; color: #8b949e;">
                Upload the old and new regulation PDFs in the sidebar, then click
                <strong style="color:#2f81f7;">Run Compliance Audit</strong>.
            </div>
        </div>
    """, unsafe_allow_html=True)

else:
    if old_pdf and new_pdf:
        if not (os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")):
            st.error("Missing API key. Set GOOGLE_API_KEY or GEMINI_API_KEY in your .env file.")
            st.stop()

        with st.spinner("AI agents are analysing documents and scoring risks…"):
            with open("temp_old.pdf", "wb") as f:
                f.write(old_pdf.getbuffer())
            with open("temp_new.pdf", "wb") as f:
                f.write(new_pdf.getbuffer())

            orchestrator = ReguGuardOrchestrator()
            results = orchestrator.run_compliance_check(
                "temp_old.pdf", "temp_new.pdf", current_profile
            )

        # Success banner
        st.markdown("""
            <div style="background: rgba(63,185,80,0.1); border: 1px solid #3fb950;
                        border-radius: 8px; padding: 14px 20px; margin-bottom: 24px;
                        display: flex; align-items: center; gap: 10px;">
                <span style="font-size:18px">✅</span>
                <span style="font-weight:600; color:#3fb950;">Analysis Complete</span>
                <span style="color:#8b949e; font-size:13px; margin-left:4px;">
                    — Scroll through the tabs below to review findings.
                </span>
            </div>
        """, unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs([
            "📄  Executive Summary",
            "🔍  Detailed Audit Trail",
            "🛠️  Action Items"
        ])

        with tab1:
            st.markdown("""
                <div style="margin-bottom:16px;">
                    <span style="font-size:11px; font-weight:600; letter-spacing:1px;
                                 text-transform:uppercase; color:#8b949e;">
                        Final Compliance Report
                    </span>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(
                f'<div class="rg-report-card">{results["report"]}</div>',
                unsafe_allow_html=True
            )

        with tab2:
            st.markdown("""
                <div style="background: rgba(47,129,247,0.06); border: 1px solid rgba(47,129,247,0.2);
                            border-radius: 8px; padding: 12px 16px; margin-bottom: 20px;
                            font-size: 13px; color: #8b949e;">
                    🔒 Every decision made by the AI is logged here for regulatory transparency.
                </div>
            """, unsafe_allow_html=True)
            col_a, col_b = st.columns(2, gap="medium")
            with col_a:
                st.markdown('<div class="rg-audit-card"><div class="rg-audit-title">Risk Evaluation Logic</div>', unsafe_allow_html=True)
                st.markdown(results['audit_trail']['risk_evaluation'])
                st.markdown('</div>', unsafe_allow_html=True)
            with col_b:
                st.markdown('<div class="rg-audit-card"><div class="rg-audit-title">Applicability Reasoning</div>', unsafe_allow_html=True)
                st.markdown(results['audit_trail']['applicability'])
                st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown(f"""
                <div style="background: rgba(210,153,34,0.08); border: 1px solid #d29922;
                            border-radius: 8px; padding: 14px 20px; margin-bottom: 20px;
                            display:flex; align-items:center; gap:10px;">
                    <span style="font-size:18px">⚠️</span>
                    <span style="font-weight:600; color:#d29922;">
                        Immediate actions required for {current_profile.company_name}
                    </span>
                </div>
            """, unsafe_allow_html=True)

            action_items = results['report'].split("### Action Items")[-1]
            st.markdown(action_items)

            st.divider()
            st.button("📥 Download PDF Report")

    else:
        st.markdown("""
            <div style="background: rgba(248,81,73,0.08); border: 1px solid #f85149;
                        border-radius: 8px; padding: 14px 20px; display:flex;
                        align-items:center; gap:10px;">
                <span style="font-size:18px">❌</span>
                <span style="font-weight:500; color:#f85149;">
                    Please upload <strong>both</strong> the Old and New regulation PDFs to proceed.
                </span>
            </div>
        """, unsafe_allow_html=True)
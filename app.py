import streamlit as st

st.markdown("""
<style>

/* ===============================
   GLOBAL THEME & BACKGROUND
================================ */
/* Base app background */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    color: #e2e8f0;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background: #0F1116 !important;
    backdrop-filter: blur(12px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

/* ===============================
   HEADERS & TYPOGRAPHY
================================ */
h1 {
    background: linear-gradient(90deg, #f97316 0%, #ec4899 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 800 !important;
    letter-spacing: -0.5px;
    padding-bottom: 10px;
}
            
h2 {
    color: #38bdf8 !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
}            

h3 {
    color: #f8fafc !important;
    font-weight: 600 !important;
}             
            
p, li, span {
    color: #cbd5e1 !important;
}

/* Override default st.write font colors that can get stuck */
.stMarkdown p {
    color: #cbd5e1 !important;
}

/* ===============================
   KPI / METRIC CARDS
================================ */
div[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-2px);
    border-color: rgba(56, 189, 248, 0.4);
}

/* Metric label (Title) */
div[data-testid="stMetric"] label {
    color: #94a3b8 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
}

/* Metric value */
div[data-testid="stMetric"] div {
    color: #ffffff !important;
    font-size: 20px !important;
    font-weight: 700 !important;
    line-height: 1.2;
}

/* Metric delta (Up/Down indicator) */
div[data-testid="stMetricValue"] + div {
    font-size: 14px !important;
    font-weight: 500 !important;
}


/* ===============================
   SECTION CARDS (.card CLASS)
================================ */
.card {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-radius: 20px;
    padding: 24px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    margin-bottom: 20px;
}

/* ===============================
   DIVIDERS
================================ */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(
        to right,
        transparent,
        rgba(255, 255, 255, 0.15),
        transparent
    );
    margin: 30px 0;
}

/* ===============================
   CHARTS & VISUALS
================================ */
/* Remove white backgrounds from default streamlit elements */
div[data-testid="stVegaLiteChart"],
div[data-testid="stPlotlyChart"],
div[data-testid="stAltairChart"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

div[data-testid="stVegaLiteChart"] svg,
div[data-testid="stPlotlyChart"] svg {
    background: transparent !important;
}

/* Tweak selectbox and input styling for dark theme */
div[data-baseweb="select"] > div {
    background-color: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: white;
    border-radius: 8px;
}

div[data-baseweb="popover"] > div {
    background-color: #1e293b;
}

/* ===============================
   ADVANCED THEMING (GLOWS & SCROLLBARS)
================================ */

/* Custom Scrollbar for Webkit */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.4);
}

/* Sidebar Navigation Items (Hover & Active States) */
div[data-testid="stSidebarNav"] li div {
    border-radius: 10px;
    transition: all 0.3s ease;
    margin: 2px 10px;
}
/* Hover state for sidebar links */
div[data-testid="stSidebarNav"] li div:hover {
    background-color: rgba(255, 255, 255, 0.1) !important;
    transform: translateX(4px);
}
/* Active state for sidebar links */
div[data-testid="stSidebarNav"] li div[data-testid="stSidebarNavLink"][aria-current="page"] {
    background: linear-gradient(90deg, rgba(236, 72, 153, 0.15) 0%, rgba(249, 115, 22, 0.15) 100%) !important;
    border-left: 3px solid #f97316;
}

/* Streamlit Primary Button override */
button[kind="primary"] {
    background: linear-gradient(90deg, #f97316 0%, #ec4899 100%) !important;
    border: none !important;
    color: white !important;
    border-radius: 8px !important;
    transition: all 0.3s ease !important;
}
button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(249, 115, 22, 0.4) !important;
}

/* Subtle Glow behind main cards to enhance glassmorphism */
.card {
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3), 0 0 20px rgba(56, 189, 248, 0.05);
}
div[data-testid="stMetric"] {
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3), 0 0 15px rgba(236, 72, 153, 0.03);
}

</style>
""", unsafe_allow_html=True)


st.set_page_config(layout="wide")



pages = [
    st.Page("home.py", title="Home", icon=":material/home:"),
    st.Page("overall.py", title="Overall Analytics", icon=":material/monitoring:"),
    st.Page("players.py", title="Player Analytics", icon=":material/groups:"),
    st.Page("teams.py", title="Team Analytics", icon=":material/group_work:")
]

selected_page = st.navigation(pages=pages, position="sidebar")
selected_page.run()
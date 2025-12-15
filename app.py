import streamlit as st

st.markdown("""
<style>

            
            


/* ===============================
   HEADERS & TEXT
================================ */
.stApp {
        background-color: #010125;
        color: #010125;
    }




h1 {
    color: red !important;
    font-weight: 700;
}
            
h2 {
    color: #82DDE4! important;
    font-weight: 700;
}            

h3 {
    color: white !important;
    font-weight: 700;
}             
            
p, li, span {
    color: #CBD5E1 !important;
}

/* ===============================
   KPI / METRIC CARDS (FIXED)
================================ */
div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(14px);
    border-radius: 18px;
    padding: 18px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 12px 30px rgba(0,0,0,0.35);
}

/* Metric label */
div[data-testid="stMetric"] label {
    color: #CBD5E1 !important;
    font-size: 10px;
}

/* Metric value */
div[data-testid="stMetric"] div {
    color: #FFFFFF !important;
    font-size: 25px;
    font-weight: 700;
}


/* ===============================
   SECTION CARDS (.card CLASS)
================================ */
.card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(16px);
    border-radius: 20px;
    padding: 22px;
    border: 1px solid rgba(255,255,255,0.12);
    box-shadow: 0 10px 35px rgba(0,0,0,0.4);
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
        rgba(255,255,255,0.25),
        transparent
    );
}

/* ===============================
   REMOVE BACKGROUND FROM CHARTS
================================ */

/* Streamlit native charts */
div[data-testid="stVegaLiteChart"],
div[data-testid="stPlotlyChart"],
div[data-testid="stAltairChart"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* SVG canvas inside charts */
div[data-testid="stVegaLiteChart"] svg,
div[data-testid="stPlotlyChart"] svg {
    background: transparent !important;
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

selected_page = st.navigation(pages=pages, position="top")
selected_page.run()
import streamlit as st
import preprocess as pre

# -------------------------------------------------------
# PAGE STYLE — IPL THEME
# -------------------------------------------------------



# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------
df, df_match = pre.preprocess_data("data/matches.csv", "data/deliveries.csv")

# -------------------------------------------------------
# SIDEBAR (INFO ONLY)
# -------------------------------------------------------
st.sidebar.subheader(" IPL Analytics")

st.sidebar.write(
    """
    Interactive analytics platform to explore
    **Indian Premier League (IPL)** data.

    Seasons covered: **2008–2024**
    """
)

st.sidebar.markdown("---")

st.sidebar.markdown("###  Data Snapshot")
st.sidebar.write(f"**Matches:** {df_match['match_id'].nunique()}")
st.sidebar.write(f"**Deliveries:** {len(df)}")

st.sidebar.markdown("---")

st.sidebar.markdown("###  Sections")
st.sidebar.write(" Overall Analytics")
st.sidebar.write(" Team Analytics")
st.sidebar.write(" Player Analytics")

st.sidebar.markdown("---")
st.sidebar.caption("📌 Data Source: Kaggle IPL Dataset")

# -------------------------------------------------------
# MAIN CONTENT
# -------------------------------------------------------
st.title("🏏 IPL Analytics Dashboard")
st.write(
    """
    The **Indian Premier League (IPL)** is one of the world’s most competitive and data-rich
    T20 cricket leagues, featuring elite players, diverse playing conditions, and evolving
    team strategies across seasons.

    This dashboard analyzes **IPL match and ball-by-ball data from 2008 to 2024** to uncover
    patterns in team dominance, player performance, venue characteristics, and match outcomes.
    """
)
st.markdown("---")
st.subheader("League • Team • Player Insights (2008–2024)")

st.write(
    """
    Explore **league-wide trends**, **team performance**, and **player insights**
    from the Indian Premier League using interactive analytics.
    """
)

st.markdown("---")

# -------------------------------------------------------
# KPI SECTION
# -------------------------------------------------------
st.markdown("##  IPL at a Glance")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("Total Matches", df_match["match_id"].nunique())

with c2:
    st.metric("Seasons Covered", df_match["season"].nunique())

with c3:
    teams = set(df_match["team1"]).union(set(df_match["team2"]))
    st.metric("Teams", len(teams))

with c4:
    st.metric("Deliveries Bowled", len(df))

st.markdown("---")

# -------------------------------------------------------
# SECTION CARDS
# -------------------------------------------------------
st.markdown("##  Explore the Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="card">
            <h3> Overall Analytics</h3>
            <ul>
                <li>IPL Titles Won</li>
                <li>Team win percentages</li>
                <li>Matches Per Season</li>
                <li>Best Venues</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="card">
            <h3> Team Analytics</h3>
            <ul>
                <li>Season-wise performance</li>
                <li>Win percentage trends</li>
                <li>Batting & bowling peaks</li>
                <li>Opponent analysis</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="card">
            <h3> Player Analytics</h3>
            <ul>
                <li>Top run scorers</li>
                <li>Top wicket takers</li>
                <li>Strike rate & economy</li>
                <li>Season & venue splits</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")

st.caption("Built using Pandas, Plotly and Streamlit.")

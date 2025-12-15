import streamlit as st
import helper as hp
import preprocess as pre
import pandas as pd
import plotly.express as px





# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------
st.set_page_config(page_title="Overall Analytics", layout="wide")


# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------
df, df_match = pre.preprocess_data("data/matches.csv", "data/deliveries.csv")

# -------------------------------------------------------
# GLOBAL FILTERS (Sidebar)
# -------------------------------------------------------
global_filters = hp.render_sidebar_global(df_match)
                

# Apply season filter
if global_filters["season"]!="All Seasons":
    df_match = df_match[df_match["season"] == global_filters["season"]]
    df = df[df["season"] == global_filters["season"]]




# Apply venue filter
if global_filters["city"] != "All Cities":
    df_match = df_match[df_match["city"] == global_filters["city"]]
    df = df[df["city"] == global_filters["city"]]




# -------------------------------------------------------
# HEADER
# -------------------------------------------------------
st.title(" Overall IPL Analytics (League-Wide)")

st.write("Explore league-wide trends, team performance, top players, and historical IPL patterns.")


# -------------------------------------------------------
# KPIs (League Summary)
# -------------------------------------------------------
if len(df_match)==0:
    st.warning("No matches were played.")
    st.stop()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Total Matches", len(df_match))

with c2:
    st.metric("Total Runs", int(df["total_runs"].sum()))

with c3:
    st.metric("Total Wickets", int(df["dismissal_kind"].notna().sum()))




# WINNER COUNT
st.markdown("---")
st.markdown("##  IPL Final Winners (Titles Won)")

finals = df_match[df_match["match_type"] == "Final"]

titles = (
    finals.groupby("winner")
    .size()
    .reset_index(name="Titles")
    .sort_values("Titles", ascending=True)
)

fig = px.bar(
    titles,
    x="Titles",
    y="winner",
    orientation="h",
    title="IPL Titles Won by Team",
    color="Titles",
    color_continuous_scale="YlOrRd"
)

st.plotly_chart(fig, use_container_width=True)




# WINNER BY SEASON
st.markdown("---")
st.markdown("##  IPL Champions by Season")

fig = px.scatter(
    finals,
    x="season",
    y="winner",
    title="IPL Champions by Season",
    color="winner",
    size=[12] * len(finals),
)


fig.update_layout(showlegend=False)

st.plotly_chart(fig, use_container_width=True)


# -------------------------------------------------------
# 1️⃣ MATCHES PER TEAM
# -------------------------------------------------------
st.markdown("---")
st.markdown("##  Matches Per Season")

matches_per_season = (
    df_match.groupby("team1")
    .size()
    .reset_index(name="matches")
)

fig = px.bar(
    matches_per_season,
    x="team1",
    y="matches",
    title="Matches Played Per Season",
    color="matches",
    color_continuous_scale="Blues"
)



st.plotly_chart(fig, use_container_width=True)


# -------------------------------------------------------
# 2️⃣ TEAM-WISE WIN PERCENTAGE
# -------------------------------------------------------
st.markdown("---")
st.markdown("##  Team-wise Win Percentage")

teams = sorted(set(df_match["team1"]).union(set(df_match["team2"])))

win_stats = []

for team in teams:
    played = df_match[
        (df_match["team1"] == team) | (df_match["team2"] == team)
    ]
    wins = df_match[df_match["winner"] == team]

    played_count = len(played)
    win_count = len(wins)
    
    win_stats.append({
        "Team": team,
        "Win %": round((win_count / played_count) * 100, 2) if played_count > 0 else 0
    })

win_df = (
    pd.DataFrame(win_stats)
    .sort_values("Win %", ascending=True)
)



fig = px.bar(
    win_df,
    x="Win %",
    y="Team",
    orientation="h",
    title="Team-wise Win Percentage",
    color="Win %",
    color_continuous_scale="Viridis"
)




st.plotly_chart(fig, use_container_width=True)



# -------------------------------------------------------
# 5️⃣ BEST VENUES FOR RUNS
# -------------------------------------------------------
st.markdown("---")
st.markdown("##  Best Batting Venues (Most Runs)")

venue_runs = (
    df.groupby("city")["total_runs"]
    .sum()
    .reset_index()
    .sort_values("total_runs", ascending=False)
    .head(10)
)

fig = px.pie(
    venue_runs,
    names="city",
    values="total_runs",
    title="Top 10 Venues by Total Runs",
    hole=0.45
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)


st.plotly_chart(fig, use_container_width=True)





# END
st.markdown("---")
st.caption("Built using Pandas, Plotly and Streamlit.")

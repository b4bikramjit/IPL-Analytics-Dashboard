# teams.py
import streamlit as st
import helper as hp
import preprocess as pre
import pandas as pd
import plotly.express as px
# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------
st.set_page_config(page_title="Team Analytics", layout="wide")

# -------------------------------------------------------
# TOP NAVIGATION BAR
# -------------------------------------------------------

# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------
df, df_match = pre.preprocess_data('data/matches.csv', 'data/deliveries.csv')


# -------------------------------------------------------
# SIDEBAR - GLOBAL FILTERS
# -------------------------------------------------------
global_filters = hp.render_sidebar_global(df_match)


    
teams_list = ["All Teams"] +  hp.get_unique_sorted(df, 'batting_team')

# -------------------------------------------------------
# SIDEBAR - TEAM FILTERS
# -------------------------------------------------------
team_filters = hp.render_sidebar_section("Team", teams_list)
team_mode = team_filters["team_mode"]
opponent = team_filters["opponent"]
selected_team = st.selectbox('Please select a Team', hp.get_unique_sorted(df, 'batting_team'))

# -------------------------------------------------------
# MAIN TITLE
# -------------------------------------------------------
st.title(" Team Analytics")
st.write('Analyze specific team performance across seasons, venues, and opponents.')








# -------------------------------------------------------
# ANALYTICS SECTION




# -------------------------------
# TEAM-LEVEL FILTERS
# -------------------------------
df = df[(df["batting_team"] == selected_team) | (df["bowling_team"] == selected_team)]
df_match = df_match[(df_match["team1"] == selected_team) | (df_match["team2"] == selected_team)]

# Opponent filter
if opponent != "All Teams":
    df = df[(df["batting_team"] == opponent) | (df["bowling_team"] == opponent)]
    df_match = df_match[(df_match["team1"] == opponent) | (df_match["team2"] == opponent)]

# Season filter
if global_filters["season"] != "All Seasons":
    df = df[df["season"] == global_filters["season"]]
    df_match = df_match[df_match["season"] == global_filters["season"]]

# City filter
if global_filters["city"] != "All Cities":
    df = df[df["city"] == global_filters["city"]]
    df_match = df_match[df_match["city"] == global_filters["city"]]

if len(df_match)==0:
    st.warning("No matches were played.")
    st.stop()

# -------------------------------
# 1️⃣ MATCHES PER SEASON
# -------------------------------


st.markdown("---")
st.markdown("##  Matches Played Per Season")

matches_per_season = (
    df_match.groupby("season")
    .size()
    .reset_index(name="matches")
)

fig = px.bar(
    matches_per_season,
    x="season",
    y="matches",
    title="Matches Played Per Season",
    color="matches",
    color_continuous_scale="Blues"
)


st.plotly_chart(fig, use_container_width=True)


# -------------------------------
# 2️⃣ WIN PERCENTAGE PER SEASON
# -------------------------------
if "winner" in df_match.columns:
    st.markdown("---")
    st.markdown("##  Win Percentage per Season")

    df_match["is_win"] = (df_match["winner"] == selected_team).astype(int)

    win_pct = (
        df_match.groupby("season")["is_win"]
        .mean()
        .reset_index()
    )
    win_pct["Win %"] = win_pct["is_win"] * 100

    fig = px.line(
        win_pct,
        x="season",
        y="Win %",
        markers=True,
        title=f"Win Percentage per Season — {selected_team}"
    )

   
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Winner column missing in dataset.")


# -------------------------------
# 3️⃣ TOP SCORES (BATTING)
# -------------------------------
if team_mode == "Batting":
    st.markdown("---")
    st.markdown("##  Highest Team Scores")

    df_bat = df[df["batting_team"] == selected_team]

    team_scores = (
        df_bat.groupby(["match_id", "inning"])["total_runs"]
        .sum()
        .reset_index()
        .sort_values("total_runs", ascending=False)
        .head(10)
    )

    st.dataframe(team_scores, hide_index='True', column_order=('total_runs', 'inning', 'match_id'), column_config={'match_id':None, 'total_runs':'Total Runs', 'inning':'Inning'})



if team_mode == "Bowling":
    st.markdown("---")
    st.markdown("##  Team Bowling Economy per Season")

    # Filter bowling data for selected team
    df_bowl = df[df["bowling_team"] == selected_team]

    # Aggregate runs conceded & balls bowled per season
    runs_conceded = (
        df_bowl.groupby("season")["total_runs"]
        .sum()
        .reset_index(name="runs_conceded")
    )

    balls_bowled = (
        df_bowl.groupby("season")["ball"]
        .count()
        .reset_index(name="balls_bowled")
    )

    econ_df = runs_conceded.merge(balls_bowled, on="season")
    econ_df["Economy"] = econ_df["runs_conceded"] / (econ_df["balls_bowled"] / 6)

    # Plot
    fig = px.line(
        econ_df,
        x="season",
        y="Economy",
        markers=True,
        title=f"Bowling Economy Trend — {selected_team}"
    )

    st.plotly_chart(fig, use_container_width=True)




# -------------------------------------------------------
# END
# -------------------------------------------------------
st.markdown("---")
st.caption("Built using Pandas, Plotly and Streamlit.")

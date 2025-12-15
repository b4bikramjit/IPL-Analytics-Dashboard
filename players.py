import streamlit as st
import helper as hp
import preprocess as pre
import pandas as pd
import plotly.express as px

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------
st.set_page_config(page_title="Player Analytics", layout="wide")



# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------
df, df_match = pre.preprocess_data("data/matches.csv", "data/deliveries.csv")

# -------------------------------------------------------
# GLOBAL FILTERS (season, venue, match type)
# -------------------------------------------------------
global_filters = hp.render_sidebar_global(df_match)

# Season filter
if global_filters["season"] != "All Seasons":
    df = df[df["season"] == global_filters["season"]]
    df_match = df_match[df_match["season"] == global_filters["season"]]

# Venue filter
if global_filters["city"] != "All Cities":
    df_match = df_match[df_match["city"] == global_filters["city"]]
    df = df[df["city"] == global_filters["city"]]


# -------------------------------------------------------
# PLAYER SECTION FILTERS (team, opponent, role)
# -------------------------------------------------------
teams =  ["All Teams"] +  hp.get_unique_sorted(df, 'batting_team')

section_filters = hp.render_sidebar_section("Player Analytics", teams)

role = section_filters["role"]
opponent = section_filters["opponent"]    # rename for clarity
team = section_filters["team"]    # global team filter

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------
st.title(" Player Analytics")
st.write("Analyze player performance across seasons, venues, and opponents.")

# -------------------------------------------------------
# APPLY PLAYER-LEVEL FILTERS
# -------------------------------------------------------

# Filter by team (section filter)
if team != "All Teams":
    df = df[(df["batting_team"] == team) | (df["bowling_team"] == team)]

# Filter by opponent (section filter)
if opponent != "All Teams":
    df = df[(df["batting_team"] == opponent) | (df["bowling_team"] == opponent)]

if len(df_match)==0:
    st.warning("No matches were played.")
    st.stop()

# -------------------------------------------------------
# BATTING ANALYTICS
# -------------------------------------------------------
if role == "Batter":
    st.markdown("---")
   

    if team != "All Teams":
        df = df[df["batting_team"] == team]

    # -----------------------------
    # TOP RUN SCORERS → BAR CHART
    # -----------------------------
    df_runs = (
        df.groupby("batter")["total_runs"]
        .sum()
        .reset_index()
        .sort_values("total_runs", ascending=False)
        .head(15)
    )

    st.markdown("##  Top Run Scorers")

    fig = px.bar(
        df_runs,
        x="total_runs",
        y="batter",
        orientation="h",
        color="total_runs",
        color_continuous_scale="Reds",
        title="Top 15 Run Scorers"
    )
    
    fig.update_layout(yaxis=dict(autorange="reversed"))
    
    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # STRIKE RATE → SCATTER PLOT
    # -----------------------------
    df_balls = df.groupby("batter")["ball"].count().reset_index(name="balls_faced")
    df_sr = df_runs.merge(df_balls, on="batter")
    df_sr["Strike Rate"] = (df_sr["total_runs"] / df_sr["balls_faced"]) * 100
    st.markdown("---")
    st.markdown("##  Runs vs Strike Rate")

    fig = px.scatter(
        df_sr,
        x="total_runs",
        y="Strike Rate",
        size="balls_faced",
        hover_name="batter",
        color="Strike Rate",
        color_continuous_scale="Turbo",
        title="Strike Rate vs Total Runs"
    )

    
    st.plotly_chart(fig, use_container_width=True)


# -------------------------------------------------------
# BOWLING ANALYTICS
# -------------------------------------------------------
elif role == "Bowler":
    st.markdown("---")
    

    if team != "All Teams":
        df = df[df["bowling_team"] == team]

    dismissals = [
        "bowled","caught","caught and bowled","hit wicket",
        "lbw","obstructing the field","stumped"
    ]

    df_wk = df[df["dismissal_kind"].isin(dismissals)].copy()
    df_wk["is_wicket"] = 1

    # -----------------------------
    # TOP WICKET TAKERS → BAR CHART
    # -----------------------------
    bowler_stats = (
        df_wk.groupby("bowler")["is_wicket"]
        .sum()
        .reset_index()
        .sort_values("is_wicket", ascending=False)
        .head(15)
    )

    st.markdown("##  Top Wicket Takers")

    fig = px.bar(
        bowler_stats,
        x="is_wicket",
        y="bowler",
        orientation="h",
        color="is_wicket",
        color_continuous_scale="Blues",
        title="Top 15 Wicket Takers"
    )

    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # ECONOMY RATE → SCATTER PLOT
    # -----------------------------
    df_runs_conc = df.groupby("bowler")["total_runs"].sum().reset_index(name="runs_conceded")
    df_balls = df.groupby("bowler")["ball"].count().reset_index(name="balls_bowled")

    df_eco = df_runs_conc.merge(df_balls, on="bowler")
    df_eco["Economy"] = df_eco["runs_conceded"] / (df_eco["balls_bowled"] / 6)

    df_eco = df_eco[df_eco["balls_bowled"] > 120]  # min overs filter
    st.markdown("---")
    st.markdown("##  Economy vs Overs Bowled")

    fig = px.scatter(
        df_eco,
        x="balls_bowled",
        y="Economy",
        hover_name="bowler",
        size="balls_bowled",
        color="Economy",
        color_continuous_scale="Viridis",
        title="Economy Rate vs Workload"
    )

    
    st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------
# FIELDING ANALYTICS
# -------------------------------------------------------
elif role == "Fielder":
    st.markdown("---")
    

    if team != "All Teams":
        df = df[df["bowling_team"] == team]

    df_field = (
        df[df["fielder"].notna()]
        .groupby("fielder")
        .size()
        .reset_index(name="dismissals")
        .sort_values("dismissals", ascending=False)
        .head(15)
    )

    st.markdown("## Most Catches / Run-outs")

    fig = px.bar(
        df_field,
        x="dismissals",
        y="fielder",
        orientation="h",
        color="dismissals",
        color_continuous_scale="Purples",
        title="Top Fielders by Dismissals"
    )

    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

st.caption("Built using Pandas, Plotly and Streamlit.")    
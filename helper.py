import streamlit as st
import pandas as pd
import preprocess as pre

df, df_match = pre.preprocess_data('data/matches.csv', 'data/deliveries.csv')

# ---------------------------------------
# BASIC UTILITY FUNCTIONS
# ---------------------------------------

def get_unique_sorted(df, col):
    """Return unique sorted values of a column."""
    try:
        values = sorted(df[col].dropna().unique().tolist())
    except:
        values = []
    return values

# Teams
teams_list = ["All Teams"] +  get_unique_sorted(df, 'batting_team')
# ---------------------------------------
# GLOBAL SIDEBAR FILTERS
# ---------------------------------------

def render_sidebar_global(df):
    st.sidebar.subheader(" Global Filters")

    # Seasons
    seasons = ["All Seasons"] + get_unique_sorted(df, "season")
    selected_season = st.sidebar.selectbox(
        "Select Season(s)", seasons, 
    )

    

    # city
    cities = ["All Cities"] + get_unique_sorted(df, "city")
    selected_city = st.sidebar.selectbox("City", cities)

   

    st.sidebar.markdown("---")

    return {
        "season": selected_season,
        
        "city": selected_city,
       
    }


    
# ---------------------------------------
# SECTION-SPECIFIC FILTERS
# ---------------------------------------

def render_sidebar_section(section_name, teams_list):
    
  

    if section_name in ["Team", "Team Analytics"]:
        st.sidebar.subheader(" Team Filters")
        team_mode = st.sidebar.radio(
            "Analysis Mode", ["Batting", "Bowling"]
        )

       

        opponent = st.sidebar.selectbox(
            "Opponent Team",
            teams_list
        )
        
        
        return {
            "team_mode": team_mode,
            "opponent": opponent,
            
        }

    elif section_name in ["Player", "Player Analytics"]:
        st.sidebar.subheader(" Player Filters")
        role = st.sidebar.radio(
            "Player Role", ["Batter", "Bowler", "Fielder"]
        )

        team= st.sidebar.selectbox(
            "Team",
            teams_list
        )

        opponent = st.sidebar.selectbox(
            "Opponent Team",
            teams_list
        )
        
        
        return {
            "role": role,
            "opponent": opponent,
            "team": team
        }

   
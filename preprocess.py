import pandas as pd

def preprocess_data(matches_path, deliveries_path):
    df_match = pd.read_csv(matches_path)
    df_del = pd.read_csv(deliveries_path)

   
    
    df_match.replace({'season': {"2020/21": "2020", "2009/10": "2010", "2007/08": "2008"}}, inplace=True)
    team_map ={"Mumbai Indians":"Mumbai Indians",
          "Chennai Super Kings":"Chennai Super Kings",
          "Kolkata Knight Riders":"Kolkata Knight Riders",
          "Royal Challengers Bangalore":"Royal Challengers Bangalore",
          "Royal Challengers Bengaluru":"Royal Challengers Bangalore",
          "Rajasthan Royals":"Rajasthan Royals",
          "Kings XI Punjab":"Kings XI Punjab",
          "Punjab Kings":"Kings XI Punjab",
          "Sunrisers Hyderabad":"Sunrisers Hyderabad",
          "Deccan Chargers":"Sunrisers Hyderabad",
          "Delhi Capitals":"Delhi Capitals",
          "Delhi Daredevils":"Delhi Capitals",
          "Gujarat Titans":"Gujarat Titans",
          "Gujarat Lions":"Gujarat Titans",
          "Lucknow Super Giants":"Lucknow Super Giants",
          "Pune Warriors":"Pune Warriors",
          "Rising Pune Supergiant":"Pune Warriors",
          "Rising Pune Supergiants":"Pune Warriors",
          "Kochi Tuskers Kerala":"Kochi Tuskers Kerala"}

    #For Match table 
    df_match['team1']= df_match['team1'].map(team_map)
    df_match['team2']= df_match['team2'].map(team_map)
    df_match['winner']= df_match['winner'].map(team_map)
    df_match['toss_winner']= df_match['toss_winner'].map(team_map)

    #For Deliverise Tables 
    df_del['batting_team']= df_del['batting_team'].map(team_map)
    df_del['bowling_team']= df_del['bowling_team'].map(team_map)

    #city
    df_match.loc[(df_match['city'].isna()) & (df_match['venue'] == 'Sharjah Cricket Stadium'), 'city'] = 'Sharjah'
    df_match.loc[(df_match['city'].isna()) & (df_match['venue'] == 'Dubai International Cricket Stadium'), 'city'] = 'Dubai'

    df_match= df_match[['id', 'season', 'city', 'match_type', 'team1', 'team2', 'winner', 'result', 'result_margin']].rename(columns={'id':'match_id'})
    df_del=df_del.drop(columns=['extra_runs', 'extras_type'])
    df_del = df_del.merge(df_match,on="match_id",)
    df = df_del


    return df, df_match


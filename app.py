import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# --------------------------------------------------------------
# Import and clean data
game_details = pd.read_csv('~/Projects/nba-python/data/games_details.csv')
print(game_details.head(5))
game_details.drop(['GAME_ID','TEAM_ID','PLAYER_ID','START_POSITION','COMMENT','TEAM_ABBREVIATION'],axis = 1,inplace= True)
game_details['FTL'] = game_details['FTA'] - game_details['FTM']
game_details = game_details.dropna()
# game_details.shape
# game_details.info()


game_details['MIN'] = game_details['MIN'].str.strip(':').str[0:2]
df = game_details.copy()

print(df.head(5))

stats_cols = {
    'FGM':'Field Goals Made',
    'FGA':'Field Goals Attempted',
    'FG_PCT':'Field Goal Percentage',
    'FG3M':'Three Pointers Made',
    'FG3A':'Three Pointers Attempted',
    'FG3_PCT':'Three Point Percentage',
    'FTM':'Free Throws Made',
    'FTA':'Free Throws Attempted',
    'FT_PCT':'Free Throw Percentage',
    'OREB':'Offensive Rebounds',
    'DREB':'Defensive Rebounds',
    'REB':'Rebounds',
    'AST':'Assists',
    'TO':'Turnovers',
    'STL':'Steals',
    'BLK':'Blocked Shots',
    'PF':'Personal Foul',
    'PTS':'Points',
    'PLUS_MINUS':'Plus-Minus'
}

def agg_on_columns(df, agg_var, operation=['mean']):
    return df[agg_var].agg(operation)

# # Remove players that didn't played at a game
# df_tmp = df[df['MIN'].isna()]
# # df_test = df[game_details['MIN']]
# print(df_tmp.head(5))
# # del df_tmp['MIN']
# # print(df_tmp.head(5))
# # # print(df_tmp.head())

# Define key statistics columns, one for percentage variable and one for other important statistics
prct_var = ['FG_PCT', 'FG3_PCT', 'FT_PCT']
other_var = ['REB', 'AST', 'STL', 'PF', 'BLK'] 

# # Create a specific dataset for LeBron James
lebron_james_df = df[df['PLAYER_NAME'] == 'LeBron James']
print(lebron_james_df.head(5))

overall_agg_prct = agg_on_columns(df=df, agg_var=prct_var, operation=['mean'])
overall_agg_other = agg_on_columns(df=df, agg_var=other_var, operation=['mean'])

lebron_james_stats_prct = agg_on_columns(df=lebron_james_df, agg_var=prct_var, operation=['mean'])
lebron_james_stats_other = agg_on_columns(df=lebron_james_df, agg_var=other_var, operation=['mean'])

def rename_df(df, col_dict):
    cols = df.columns
    new_cols = [(col_dict[c] if c in col_dict else c) for c in cols]
    df.columns = new_cols
    return df

# -----------------------------------------------------------------
# App layout
app = dash.Dash()
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(
        children='''Dash: A web application framework for Python.''')
    ])

if __name__ == "__main__":
    app.run_server(debug=True)
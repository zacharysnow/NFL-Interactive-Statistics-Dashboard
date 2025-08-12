import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
#Team statistics dataframe
url = 'https://api.sportsdata.io/v3/nfl/scores/json/TeamSeasonStats/{2024REG}?key=b3c141ba44fc4f1ab22d3200d4f8a48f'
response = requests.get(url)
data = response.json()
print(data)
df = pd.DataFrame(data)

#Player statistics dataframe
url2 = 'https://api.sportsdata.io/v3/nfl/stats/json/PlayerSeasonStats/{2024REG}?key=b3c141ba44fc4f1ab22d3200d4f8a48f'
response = requests.get(url2)
data2 = response.json()
print(data2)
df2 = pd.DataFrame(data2)

#Quarterback and passing yards dataframe
QB_df = df2[df2['Position'] == 'QB'][['PassingYards', 'Name', 'Team', 'Position']]
QB_df = QB_df.sort_values(by='PassingYards', ascending=False).head(32)

#Runningback and rushing yards dataframe
RB_df = df2[df2['Position'] == 'RB'][['RushingYards', 'Name', 'Team', 'Position']]
RB_df = RB_df.sort_values(by='RushingYards', ascending=False).head(32)

#Widereceiver and receiving yards dataframe
WR_df = df2[df2['Position'] == 'WR'][['ReceivingYards', 'Name', 'Team', 'Position']]
WR_df = WR_df.sort_values(by='ReceivingYards', ascending=False).head(32)

#Teams points per game dataframe
df['PPG'] = (df['Score']/df['Games']).round(2)
PPG_df = df[['Team', 'PPG']]
PPG_df = PPG_df.sort_values(by='PPG', ascending=False)

#Teams points allowed per game dataframe
df['PPG_allowed'] = (df['OpponentScore']/df['Games']).round(2)
PPG_allowed_df = df[['Team', 'PPG_allowed']]
PPG_allowed_df = PPG_allowed_df.sort_values(by='PPG_allowed', ascending=False)

#Teams turnover differential dataframe (higher turnover differential = better)
#We can compare the correlation between points per game(PPG_df) and turnover differential
df['Turnover_Differential'] = (df['Takeaways'] - df['Giveaways'])
Turnover_Differential_df = df[['Team', 'Turnover_Differential']]
Turnover_Differential_df = Turnover_Differential_df.sort_values(by='Turnover_Differential', ascending=False)

Turnover_Differential_PPG_df = df[['Team', 'Turnover_Differential','PPG']].copy()
print(df[['Turnover_Differential', 'PPG']].isnull().sum())
print(df['Team'].value_counts())

#Scatter plot comparing ppg_df and ppg_allowed_df
plt.figure(figsize=(8,6))
plt.scatter(df['PPG_allowed'], df['PPG'], s=100)
for i, row in df.iterrows():
    plt.text(row['PPG_allowed']+0.2, row['PPG'], row['Team'], fontsize=10)

plt.axhline(df['PPG'].mean(), color='gray', linestyle='--', linewidth=0.7)
plt.axvline(df['PPG_allowed'].mean(), color='gray', linestyle='--', linewidth=0.7)
plt.xlabel('Points Allowed per Game (PPG_allowed) - Lower is Better')
plt.ylabel('Points per Game (PPG) - Higher is Better')
plt.title('NFL Team Performance: PPG vs PPG_allowed (2024)')
plt.show()

fig = px.scatter(df,
                 x='Turnover_Differential',
                 y='PPG',
                 color='Team',
                 trendline='ols',
                 labels={'Turnover_Differential': 'Turnover Differential (Higher is Better)',
                         'PPG': 'Points Per Game (PPG)'},
                 hover_name='Team'
                )
fig2 = plt.figure()
sns.regplot(x='Turnover_Differential', y='PPG', data=Turnover_Differential_PPG_df, ci=None)
plt.title('Turnover Differential  vs PPG')
plt.show()

import dash
from dash import html
from dash import dcc

# NFL logo URL
logo_url = 'https://www.clipartmax.com/png/middle/66-667753_nfl-logo-national-football-league-logo-png.png'

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([

    # Row with logo (left) and heading (center top)
    html.Div([
        # Logo aligned left
        html.Div([
            html.Img(src=logo_url, style={
                'width': '125px',  # reduced size by 50%
                'display': 'inline-block',
                'vertical-align': 'top'
            })
        ], style={'width': '20%', 'display': 'inline-block'}),

        # Heading aligned center
        html.Div([
            html.H1('NFL 2024 Analysis', style={
                'color': 'maroon',
                'font-weight': 'bold',
                'font-size': '50px',
                'margin': '0',
                'padding-top': '15px',
                'text-align': 'center'
            })
        ], style={'width': '80%', 'display': 'inline-block'})
    ], style={'width': '100%', 'display': 'flex'}),
    #the line graph
    html.Div(
        children=[
            # Add a H3
            html.H3('Relationship between Turnover Differential and Points Per Game (2024)'),
            # Add  graph
            dcc.Graph(id='turnover_diff_vs_ppg', figure=fig, style={'width':'500px', 'height':'350px', 'margin':'auto'})
        ]),

    # Footer (bottom center)
    html.Div([
        html.I('Copyright © 2025 Zachary, Samuel, Meghana INC')
    ], style={
        'position': 'fixed',
        'bottom': '10px',
        'width': '100%',
        'text-align': 'center',
        'font-style': 'italic'
    })

], style={
    'font-size': 15,
    'position': 'relative',
    'min-height': '100vh'
})

# Run app
if __name__ == '__main__':
    app.run(debug=False)

import requests
import pandas as pd

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

<<<<<<< HEAD
import dash
from dash import html
=======
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

#Teams total touchdowns on the season or touchdowns per game dataframe?
TD_df = df[['Team', 'Touchdowns']]
TD_df = TD_df.sort_values(by='Touchdowns', ascending=False)

>>>>>>> origin/main

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

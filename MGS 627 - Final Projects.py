import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import dash
from dash import html, dcc


def fetch_nfl_data(endpoint, season, api_key):
    """
       Fetch NFL data from the SportsData.io API for a given endpoint and season.

       Parameters
       ----------
       endpoint : str
           The API endpoint path after 'nfl/' (e.g., 'scores/json/TeamSeasonStats').
       season : str
           The season code to request, in the format '2024REG', '2024PRE', or '2024POST'
           (e.g., '2024REG' for 2024 regular season).
       api_key : str
           Your SportsData.io API key for authentication.

       Returns
       -------
       pandas.DataFrame
           A DataFrame containing the JSON response from the API.

       - The returned DataFrame will vary in structure depending on the endpoint requested.
       - See SportsData.io documentation for available endpoints and their fields.
       """

    url = f"https://api.sportsdata.io/v3/nfl/{endpoint}/{{{season}}}?key={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    return pd.DataFrame(response.json())

API_KEY ='b3c141ba44fc4f1ab22d3200d4f8a48f'
#Team statistics dataframe
df = fetch_nfl_data("scores/json/TeamSeasonStats", "2024REG", API_KEY)
#Player statistics dataframe
df2 = fetch_nfl_data("stats/json/PlayerSeasonStats", "2024REG", API_KEY)
#Team statistics dataframe
# url = 'https://api.sportsdata.io/v3/nfl/scores/json/TeamSeasonStats/{2024REG}?key=b3c141ba44fc4f1ab22d3200d4f8a48f'
# response = requests.get(url)
# data = response.json()
# df = pd.DataFrame(data)

#Player statistics dataframe
# url2 = 'https://api.sportsdata.io/v3/nfl/stats/json/PlayerSeasonStats/{2024REG}?key=b3c141ba44fc4f1ab22d3200d4f8a48f'
# response = requests.get(url2)
# data2 = response.json()
# df2 = pd.DataFrame(data2)

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
df['PPG'] = (df['Score'] / df['Games']).round(2)
PPG_df = df[['Team', 'PPG']].sort_values(by='PPG', ascending=False)

#Teams points allowed per game dataframe
df['PPG_allowed'] = (df['OpponentScore'] / df['Games']).round(2)
PPG_allowed_df = df[['Team', 'PPG_allowed']].sort_values(by='PPG_allowed', ascending=False)

#Teams turnover differential dataframe (higher turnover differential = better)
#We can compare the correlation between points per game(PPG_df) and turnover differential
df['Turnover_Differential'] = (df['Takeaways'] - df['Giveaways'])
Turnover_Differential_df = df[['Team', 'Turnover_Differential']].sort_values(by='Turnover_Differential',ascending=False)
Turnover_Differential_PPG_df = df[['Team', 'Turnover_Differential', 'PPG']].copy()

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

fig = px.scatter(
    df,
    x='Turnover_Differential',
    y='PPG',
    color='Team',
    trendline='ols',
    labels={'Turnover_Differential': 'Turnover Differential (Higher is Better)', 'PPG': 'Points Per Game (PPG)'},
    hover_name='Team',
    title='Turnover Differential vs Points Per Game (2024 Season)'
)

kpi_avg_ppg = df['PPG'].mean()
kpi_max_ppg_team = PPG_df.iloc[0]
kpi_best_turnover_team = Turnover_Differential_df.iloc[0]

pass_rush_fig = px.scatter(
    df,
    x='PassingYards',
    y='RushingYards',
    color='Team',
    size='PPG',
    hover_name='Team',
    trendline='ols',
    title='Total Passing Yards vs Total Rushing Yards (2024 Season)',
    labels={'PassingYards': 'Total Passing Yards', 'RushingYards': 'Total Rushing Yards'}
)

team_qb_passing = QB_df.groupby('Team')['PassingYards'].sum().reset_index()
team_qb_passing = team_qb_passing.merge(PPG_df, on='Team', how='left')

qb_pass_vs_ppg_fig = px.scatter(
    team_qb_passing,
    x='PassingYards',
    y='PPG',
    text='Team',
    size='PPG',
    color='Team',
    trendline='ols',
    title='Total QB Passing Yards vs PPG (2024 Season)',
    labels={'PassingYards': 'Total QB Passing Yards', 'PPG': 'Points Per Game'}
)

rush_pass_td_df = df[['Team', 'RushingTouchdowns', 'PassingTouchdowns']].copy()
rush_pass_td_fig = px.bar(
    rush_pass_td_df.melt(id_vars='Team', value_vars=['RushingTouchdowns', 'PassingTouchdowns'],
                         var_name='TD Type', value_name='Touchdowns'),
    x='Team',
    y='Touchdowns',
    color='TD Type',
    barmode='group',
    title='Total Rushing Touchdowns vs Passing Touchdowns (2024 Season)'
)

# Make all graphs semi-transparent black background
for g in [fig, pass_rush_fig, qb_pass_vs_ppg_fig, rush_pass_td_fig]:
    g.update_layout(
        paper_bgcolor='rgba(0,0,0,0.5)',  # 50% opacity
        plot_bgcolor='rgba(0,0,0,0.5)',  # 50% opacity
        font_color='white',
        title_font_color='white'
    )

# NFL logo URL
logo_url = 'https://www.clipartmax.com/png/middle/66-667753_nfl-logo-national-football-league-logo-png.png'
background_url = 'https://static.clubs.nfl.com/image/private/t_new_photo_album_2x/f_auto/bills/xqkzseuxtexhhjk1jfkd.jpg'

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.Div([
            html.Img(
                src=logo_url,
                style={'width': '125px', 'display': 'inline-block', 'vertical-align': 'middle'}
            )
        ], style={'width': '20%', 'display': 'inline-block', 'text-align': 'left'}),

        html.Div([
            html.H1(
                '2024 Analysis',
                style={
                    'color': 'maroon',
                    'font-weight': 'bold',
                    'font-size': '50px',
                    'margin-right': '65px',
                    'padding-top': '15px',
                    'text-align': 'right'
                }
            )
        ], style={'width': '80%', 'display': 'inline-block', 'text-align': 'right'})
    ], style={'width': '100%', 'display': 'flex', 'align-items': 'center'}),

    html.H2("Key Performance Indicators", style={'text-align': 'center', 'color': 'white',
                                                 'backgroundColor': 'rgba(0,0,0,0.7)', 'padding': '10px'}),

    # KPI Cards
    html.Div([
        html.Div([
            html.H4("Average PPG Across Teams", style={'color': 'white'}),
            html.P(f"{kpi_avg_ppg:.2f}", style={'font-size': '24px', 'color': 'white'})
        ], style={'width': '33%', 'display': 'inline-block', 'text-align': 'center'}),
        html.Div([
            html.H4("Highest Scoring Team", style={'color': 'white'}),
            html.P(f"{kpi_max_ppg_team['Team']} ({kpi_max_ppg_team['PPG']})",
                   style={'font-size': '24px', 'color': 'white'})
        ], style={'width': '33%', 'display': 'inline-block', 'text-align': 'center'}),
        html.Div([
            html.H4("Best Turnover Differential", style={'color': 'white'}),
            html.P(f"{kpi_best_turnover_team['Team']} ({kpi_best_turnover_team['Turnover_Differential']})",
                   style={'font-size': '24px', 'color': 'white'})
        ], style={'width': '33%', 'display': 'inline-block', 'text-align': 'center'}),
    ], style={'margin': '20px 0', 'backgroundColor': 'rgba(0,0,0,0.7)', 'padding': '15px', 'border-radius': '10px'}),

    # Dropdown + Main Graph
    html.Div([
        html.H3('Select Analysis View',
                style={'color': 'white', 'backgroundColor': 'rgba(0,0,0,0.7)', 'padding': '5px'}),
        dcc.Dropdown(
            id='graph-selector',
            options=[
                {'label': 'Turnover Differential vs PPG', 'value': 'turnover'},
                {'label': 'Passing vs Rushing Yards', 'value': 'passrush'},
                {'label': 'QB Passing Yards vs PPG', 'value': 'qbpass'}
            ],
            value='turnover'
        ),
        dcc.Graph(id='main-graph', style={'width': '100%', 'height': '500px', 'margin': 'auto'})
    ]),

    # Static Bar Graph
    html.Div([
        dcc.Graph(figure=rush_pass_td_fig)
    ], style={'margin-top': '30px'}),

    # Footer (bottom center)
    html.Div([
        html.I('Copyright © 2025 Zachary, Samuel, Meghana INC', style={'color': 'white'})
    ], style={'position': 'fixed', 'bottom': '10px', 'width': '100%', 'text-align': 'center', 'font-style': 'italic'})
],
    style={
        'font-size': 15,
        'position': 'relative',
        'min-height': '100vh',
        'background-image': f'url("{background_url}")',
        'background-size': 'cover',
        'background-position': 'center',
        'background-attachment': 'fixed'
    })


@app.callback(
    dash.dependencies.Output('main-graph', 'figure'),
    [dash.dependencies.Input('graph-selector', 'value')]
)
def update_main_graph(selected):
    if selected == 'turnover':
        return fig
    elif selected == 'passrush':
        return pass_rush_fig
    elif selected == 'qbpass':
        return qb_pass_vs_ppg_fig
    return fig


if __name__ == '__main__':
    app.run(debug=False)

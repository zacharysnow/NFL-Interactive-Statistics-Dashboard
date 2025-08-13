import requests
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import dash
from dash import html, dcc

#Creating a dashboard for NFL Data season 2024 analysis by Zachary, Samuel and Meghana Summer 2025 batch


def fetch_nfl_data(endpoint, season, api_key):
    """
       This function is used to fetch NFL data from the SportsData.io API for a given endpoint and season.

       Parameters :
       endpoint : str
           The API endpoint path after 'nfl/' (e.g., 'scores/json/TeamSeasonStats').
       season : str
           The season code to request, in the format '2024REG', '2024PRE', or '2024POST'
           (e.g., '2024REG' for 2024 regular season).
       api_key : str
           Your SportsData.io API key for authentication.

       Returns :
       pandas.DataFrame
           A DataFrame containing the JSON response from the API.

       - The returned DataFrame will vary in structure depending on the endpoint requested.
       - See SportsData.io documentation for available endpoints and their fields.
        https://sportsdata.io/developers/api-documentation/nfl
       """

    url = f"https://api.sportsdata.io/v3/nfl/{endpoint}/{{{season}}}?key={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    return pd.DataFrame(response.json())
#This is  our team's API key , used to fetch the NFL data from the SportsData.io APIs
API_KEY ='b3c141ba44fc4f1ab22d3200d4f8a48f'
#Team statistics dataframe
df = fetch_nfl_data("scores/json/TeamSeasonStats", "2024REG", API_KEY)
#Player statistics dataframe
df2 = fetch_nfl_data("stats/json/PlayerSeasonStats", "2024REG", API_KEY)


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

#Teams turnover differential dataframe (higher turnover differential = better)
df['Turnover_Differential'] = (df['Takeaways'] - df['Giveaways'])
Turnover_Differential_df = df[['Team', 'Turnover_Differential']].sort_values(by='Turnover_Differential',ascending=False)
Turnover_Differential_PPG_df = df[['Team', 'Turnover_Differential', 'PPG']].copy()

#Full team names dictionary
team_names = {
    "DET": "Detroit Lions (DET)", "BUF": "Buffalo Bills (BUF)",
    "BAL": "Baltimore Ravens (BAL)",  "TB": "Tampa Bay Buccaneers (TB)", "WAS": "Washington Commanders (WAS)",
    "CIN": "Cincinnati Bengals (CIN)",  "PHI": "Philadelphia Eagles (PHI)",
    "GB": "Green Bay Packers (GB)","MIN": "Minnesota Vikings (MIN)", "DEN": "Denver Broncos (DEN)", "LAC": "Los Angeles Chargers (LAC)",
    "ARI": "Arizona Cardinals (ARI)","SF": "San Francisco 49ers (SF)",  "ATL": "Atlanta Falcons (ATL)", "KC": "Kansas City Chiefs (KC)", "PIT": "Pittsburgh Steelers (PIT)",
    "IND": "Indianapolis Colts (IND)", "SEA": "Seattle Seahawks (SEA)", "HOU": "Houston Texans (HOU)", "LAR": "Los Angeles Rams (LAR)",
    "DAL": "Dallas Cowboys (DAL)", "MIA": "Miami Dolphins (MIA)", "CAR": "Carolina Panthers (CAR)",  "NO": "New Orleans Saints (NO)",
    "NYJ": "New York Jets (NYJ)", "JAX": "Jacksonville Jaguars (JAX)", "TEN": "Tennessee Titans (TEN)",  "CHI": "Chicago Bears (CHI)",
    "LV": "Las Vegas Raiders (LV)",  "NE": "New England Patriots (NE)", "NYG": "New York Giants (NYG)",  "CLE": "Cleveland Browns (CLE)"
}

#Plotting a graph of turnoverdifferential(a team's takeaways minus their giveaways) vs the points per game
fig = px.scatter(
    df,
    x='Turnover_Differential',
    y='PPG',
    trendline='ols',
    trendline_color_override='red',
    labels={'Turnover_Differential': 'Turnover Differential (Higher is Better)', 'PPG': 'Points Per Game (PPG)'},
    hover_name='Team',
    title='Turnover Differential vs Points Per Game (2024 Season)'
)
#setting properties of the regression line for the above graph, to visualize if there is a positive correlation
#b/w turnover diff and the team's PPG
fig.update_traces(selector=dict(mode='lines'), line=dict(width=4))
fig.data = [trace for trace in fig.data if trace.mode != 'lines+markers']

#Calculating the KPI values
#average of points per game for the NFL teams
kpi_avg_ppg = df['PPG'].mean()
#The max avg of PPg
kpi_max_ppg_team = PPG_df.iloc[0]
#Finsing the best turn over differential
kpi_best_turnover_team = Turnover_Differential_df.iloc[0]

#a scatter plot for the graph to show Total passing yards vs total rushing yards across the season
pass_rush_fig = px.scatter(
    df,
    x='PassingYards',
    y='RushingYards',
    color='Team',
    text='Team',
    size='PPG',
    hover_name='Team',
    trendline='ols',
    title='Total Passing Yards vs Total Rushing Yards (2024 Season)',
    labels={'PassingYards': 'Total Passing Yards', 'RushingYards': 'Total Rushing Yards'}
)
#QB(Quarter Back) Passing Yards vs PPG
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
#Rushing Touch Downs vs Passing Touch Downs
rush_pass_td_df = df[['Team', 'RushingTouchdowns', 'PassingTouchdowns']].copy()
#plotting a bar chart for Rushing TDs vs Passing TDs
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
#Background Image URL
background_url = 'https://static.clubs.nfl.com/image/private/t_new_photo_album_2x/f_auto/bills/xqkzseuxtexhhjk1jfkd.jpg'

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    # Adding the NFL Logo on the top LHS of the dashboard
    html.Div([
        html.Div([
            html.Img(
                src=logo_url,
                style={'width': '125px', 'display': 'inline-block', 'vertical-align': 'middle'}
            )
        ], style={'width': '20%', 'display': 'inline-block', 'text-align': 'left'}),
        #DashBoard Heading
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
    #Heading for the KeyPI Section
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

        # ----- PPG Dropdown -----
    html.Div([
        html.H3("Select Team to See PPG",style={'color': 'white'}),
        dcc.Dropdown(
            id='ppg-selector',
            options=[{'label': name, 'value': abbr} for abbr, name in team_names.items()],
            value=None
        ),
        html.Div(
            id='ppg-output',
            style={'font-size': '24px', 'color': 'white', 'text-align': 'center', 'margin-top': '10px'}
        )
    ], style={'backgroundColor': 'rgba(0,0,0,0.7)', 'color': 'black', 'padding': '20px'}),

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
    """
    This function updates the main graph in the dashboard based on the selected dropdown option.

    Parameters :
    selected : str
        The value chosen from the 'graph-selector' dropdown. Expected values:
        - 'turnover': Displays the Turnover Differential vs Points Per Game (with regression line).
        - 'passrush': Displays Passing Yards vs Rushing Yards for all teams.
        - 'qbpass'  : Displays QB Passing Yards vs Points Per Game.

    Returns :

        A Plotly figure corresponding to the selected graph.


    - If the input does not match one of the expected values, the default figure shown will be the turnover figure.

    """
    if selected == 'turnover':
        return fig
    elif selected == 'passrush':
        return pass_rush_fig
    elif selected == 'qbpass':
        return qb_pass_vs_ppg_fig
    return fig

@app.callback(
    dash.dependencies.Output('ppg-output', 'children'),
    dash.dependencies.Input('ppg-selector', 'value')
)
def display_ppg(selected_team):
    """
    This function returns the points per game (PPG) for the selected NFL team.

    Parameters :
    selected_team : str
        The abbreviation or key of the team selected from a dropdown.
        Example: 'NE' for New England Patriots.

    Returns :
    str
        A string displaying the full team name and its PPG in the format:
        "{Team Name}: {PPG} PPG".
        If no team is selected, returns "Select a team to see PPG".

    Notes :
    - Uses the PPG_df DataFrame to look up the PPG value.
    - Uses the team_names dictionary to get the full team name.
    """
    if selected_team:
        ppg_value = PPG_df.loc[PPG_df['Team'] == selected_team, 'PPG'].values[0]
        return f"{team_names[selected_team]}: {ppg_value} PPG"
    return "Select a team to see PPG"

# Running the app
if __name__ == '__main__':
    app.run(debug=False)

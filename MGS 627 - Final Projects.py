import requests
import pandas as pd

url = 'https://api.sportsdata.io/v3/nfl/scores/json/TeamSeasonStats/{2024REG}?key=b3c141ba44fc4f1ab22d3200d4f8a48f'
response = requests.get(url)
data = response.json()
print(data)
df = pd.DataFrame(data)

url2 = 'https://api.sportsdata.io/v3/nfl/stats/json/PlayerSeasonStats/{2024REG}?key=b3c141ba44fc4f1ab22d3200d4f8a48f'
response = requests.get(url2)
data2 = response.json()
print(data2)
df2 = pd.DataFrame(data2)

import pandas as pd

df3 = df2[df2['Team'] == 'BUF']
print(df3)

import requests

# Setting the URL of the image to download (medium-size NFL logo)
logo_url = 'https://www.clipartmax.com/png/middle/66-667753_nfl-logo-national-football-league-logo-png.png'


# Sending a GET request to fetch the image from the URL
#response = requests.get(logo_url)

# Raise an error if the request failed
#response.raise_for_status()



# Open a file in write-binary mode to save the image locally
#with open('nfl_logo.png', 'wb') as f:
# Write the content of the image to the file
    #f.write(response.content)

# Print confirmation that the image was successfully saved
#print("NFL logo image saved as nfl_logo.png")

# Import the required Dash components
import dash
from dash import html

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
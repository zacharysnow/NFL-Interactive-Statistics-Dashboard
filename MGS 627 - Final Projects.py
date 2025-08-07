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

#Quarterback and passing yards dataframe
QB_df = df2[df2['Position'] == 'QB'][['PassingYards', 'Name', 'Team', 'Position']]
QB_df = QB_df.sort_values(by='PassingYards', ascending=False).head(32)

#Runningback and rushing yards dataframe
RB_df = df2[df2['Position'] == 'RB'][['RushingYards', 'Name', 'Team', 'Position']]
RB_df = RB_df.sort_values(by='RushingYards', ascending=False).head(32)

#Widereceiver and receiving yards dataframe
WR_df = df2[df2['Position'] == 'WR'][['ReceivingYards', 'Name', 'Team', 'Position']]
WR_df = WR_df.sort_values(by='ReceivingYards', ascending=False).head(32)


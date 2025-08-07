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

df3 = df2[df2['Position'] == 'QB'][['PassingYards', 'Name', 'Team', 'Position']]
df3 = df3.sort_values(by='PassingYards', ascending=False).head(32)


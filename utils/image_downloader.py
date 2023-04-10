"""
A small script that downloads every headshot included
in the CDL match data ot the images folder
"""
import requests
import pandas as pd

from utils.general import read_matches

df = read_matches()

heads = df['headshot'].unique()
test_df = pd.DataFrame({'headshot':heads})
heads_df = pd.merge(test_df, df[['headshot', 'alias']], how='left', on='headshot').drop_duplicates()
for headshot, alias in zip(heads_df['headshot'], heads_df['alias']):
    with open(f"images/{alias}_headshot.png", 'wb') as file:
        response = requests.get(headshot)
        file.write(response.content)
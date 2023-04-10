import pandas as pd


def declare_map_winner(df: pd.DataFrame) -> pd.DataFrame:
    df['map_winner'] = ["host" if a > b else "guest" for a, b in zip(df['matchGameResult.hostGameScore'], df['matchGameResult.guestGameScore'])]

    df['is_winner'] = ["Y" if a == b else "N" for a, b in zip(df['map_winner'], df['team_type'])]

    return df

def declare_match_winner(df: pd.DataFrame) -> pd.DataFrame:
    df['isMatchWinner'] = ['y' if a == b else 'n' for a, b in zip(df['winnerTeamId'], df['team_id'])]
    return df


def calculate_kd(df: pd.DataFrame):
    df['kd'] = df['totalKills']/df['totalDeaths']
    return df





    
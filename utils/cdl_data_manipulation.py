import pandas as pd


def get_head_to_head_player_stats(df: pd.DataFrame, team1: str, team2: str) -> pd.DataFrame:

    group_map = {var: "sum" for var in ['totalKills', 'totalDeaths', 'untradedKills',
                                        'totalFirstBloodKills', 'tradedDeaths']}
    group_map['mapKD'] = 'mean'
    group_map['hillTime'] = 'mean'
    group_map['totalDamageDealt'] = 'mean'
    group_map['firstBloodPercent'] = 'mean'
    

    # Team 1 stats
    t1_df = df[df['abbrev']==team1].copy()
    t1_df['mapKD'] = t1_df['totalKills']/t1_df['totalDeaths']
    t1_df['firstBloodPercent'] = t1_df['totalFirstBloodKills']/t1_df['totalKills']
    t1_df_h2h = t1_df.copy()[t1_df['oppo_abbrev']==team2]

    t1_kd_df = t1_df.groupby(['alias', 'abbrev']).agg(group_map).reset_index()
    t1_kd_df['overallKD'] = t1_kd_df['totalKills']/t1_kd_df['totalDeaths']
    t1_kd_df['overallTradedDeathsPercent'] = t1_kd_df['tradedDeaths']/t1_kd_df['totalDeaths']
    t1_kd_df['overallUntradedKillsPercent'] = t1_kd_df['untradedKills']/t1_kd_df['totalKills']

    t1_kd_df_h2h = t1_df_h2h.groupby(['alias', 'abbrev']).agg(group_map).reset_index()
    t1_kd_df_h2h['overallKD'] = t1_kd_df_h2h['totalKills']/t1_kd_df_h2h['totalDeaths']
    t1_kd_df_h2h['overallTradedDeathsPercent'] = t1_kd_df_h2h['tradedDeaths']/t1_kd_df_h2h['totalDeaths']
    t1_kd_df_h2h['overallUntradedKillsPercent'] = t1_kd_df_h2h['untradedKills']/t1_kd_df_h2h['totalKills']

    # Team 2 stats (could be functionalised but I cba)
    t2_df = df[df['abbrev']==team2].copy()
    t2_df['mapKD'] = t2_df['totalKills']/t2_df['totalDeaths']
    t2_df['firstBloodPercent'] = t2_df['totalFirstBloodKills']/t2_df['totalKills']
    t2_df_h2h = t2_df.copy()[t2_df['oppo_abbrev']==team1]

    t2_kd_df = t2_df.groupby(['alias', 'abbrev']).agg(group_map).reset_index()
    t2_kd_df['overallKD'] = t2_kd_df['totalKills']/t2_kd_df['totalDeaths']
    t2_kd_df['overallTradedDeathsPercent'] = t2_kd_df['tradedDeaths']/t2_kd_df['totalDeaths']
    t2_kd_df['overallUntradedKillsPercent'] = t2_kd_df['untradedKills']/t2_kd_df['totalKills']

    t2_kd_df_h2h = t2_df_h2h.groupby(['alias', 'abbrev']).agg(group_map).reset_index()
    t2_kd_df_h2h['overallKD'] = t2_kd_df_h2h['totalKills']/t2_kd_df_h2h['totalDeaths']
    t2_kd_df_h2h['overallTradedDeathsPercent'] = t2_kd_df_h2h['tradedDeaths']/t2_kd_df_h2h['totalDeaths']
    t2_kd_df_h2h['overallUntradedKillsPercent'] = t2_kd_df_h2h['untradedKills']/t2_kd_df_h2h['totalKills']
    
    # Combined
    needed_columns = ['alias', 'abbrev', 'overallKD', 'mapKD', 'overallUntradedKillsPercent', 'overallTradedDeathsPercent', 'hillTime',
                      'firstBloodPercent', 'totalDamageDealt']
    
    rename_map = {"mapKD": "averageMapKD", "hillTime": "averageMapHillTime", 
                  "firstBloodPercent": "averageMapFirstBloodPercent", "totalDamageDealt": "averageMapDamageDealt",
                  'overallKD': 'overallKD', 'overallTradedDeathsPercent': 'overallTradedDeathsPercent', 
                  'overallUntradedKillsPercent': 'overallUntradedKillsPercent'}

    t1_kd_df = t1_kd_df[needed_columns]
    t1_kd_df.rename(mapper=rename_map, inplace=True, axis='columns')

    t1_kd_df_h2h = t1_kd_df_h2h[needed_columns]
    t1_kd_df_h2h.rename(mapper=rename_map, inplace=True, axis='columns')

    t2_kd_df = t2_kd_df[needed_columns]
    t2_kd_df.rename(mapper=rename_map, inplace=True, axis='columns')

    t2_kd_df_h2h = t2_kd_df_h2h[needed_columns]
    t2_kd_df_h2h.rename(mapper=rename_map, inplace=True, axis='columns')

    t1_joined = pd.merge(t1_kd_df, t1_kd_df_h2h, how='left', on=['alias', 'abbrev'], suffixes=('_vs_all', f'_vs_{team2}'))
    t2_joined = pd.merge(t2_kd_df, t2_kd_df_h2h, how='left', on=['alias', 'abbrev'], suffixes=('_vs_all', f'_vs_{team1}'))

    return pd.concat([t1_joined, t2_joined], axis=0)

def top_overall(df: pd.DataFrame, min_maps):
    needed_columns = ["alias", "abbrev", "totalKills", "totalDeaths", "totalDamageDealt", "damageTaken", "totalAssists", "untradedKills", "tradedDeaths",
                       "untradedDeaths", "tradedKills", "bombsPlanted", "bombsDefused", "totalWallbangKills", "totalRotationKills", "totalFirstBloodKills",
                       "totalDistanceTraveled", "mapsPlayed", "hillTime", "contestedHillTime", "lethalsUsed", "tacticalsUsed"]
    df['mapsPlayed'] = 1
    grouped = df.groupby(['alias', 'abbrev']).sum().reset_index()[needed_columns]
    grouped = grouped[grouped['mapsPlayed']>=min_maps]

    grouped['overallKD'] = grouped['totalKills']/grouped['totalDeaths']
    grouped['firstBloodPerMap'] = grouped['totalFirstBloodKills']/grouped['mapsPlayed']
    grouped['hillTimePerMap'] = grouped['hillTime']/grouped['mapsPlayed']
    grouped['totalDamageDelta'] = grouped['totalDamageDealt']-grouped['damageTaken']
    grouped['percentOfKillUntraded'] = grouped['untradedKills']/grouped['totalKills']
    grouped['percentOfDeathsUntraded'] = grouped['untradedDeaths']/grouped['totalDeaths']
    grouped['percentOfKillsTraded'] = grouped['tradedKills']/grouped['totalKills']
    grouped['percentOfDeathsTraded'] = grouped['tradedDeaths']/grouped['totalDeaths']
    grouped['totalDamagePerMap'] = grouped['totalDamageDealt']/grouped['mapsPlayed']
    grouped['totalDistanceTraveledPerMap'] = grouped['totalDistanceTraveled']/grouped['mapsPlayed']

    return grouped




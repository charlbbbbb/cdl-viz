import pandas as pd

CDL_PALETTE = {'NY': 'yellow',
           'LV': 'orange',
           'BOS': '#0bf52b',
           'FLA': 'cyan',
           'MIN': 'purple',
           'TOR': '#f40afe',
           'ATL': '#f84c4c',
           'TX': 'green',
           'LAT': 'red',
           'LAG': '#7a0265',
           'SEA': 'blue',
           'LDN': '#800020'}

CDL_PALETTE_SECONDARY = {'NY': '#0e055f',
           'LV': '#f90101',
           'BOS': '#06450f',
           'FLA': '#1eb509',
           'MIN': '#b549bf',
           'TOR': '#230426',
           'ATL': '#520516',
           'TX': '#000000',
           'LAT': '#000000',
           'LAG': '#e745da',
           'SEA': '#32fbf1',
           'LDN': '#0a43f4'}

CDL_FULL_TEAM_NAMES = {'NY': 'New York Subliners',
           'LV': 'Las Vegas Legion',
           'BOS': 'Boston Breach',
           'FLA': 'Florida Mutineers',
           'MIN': 'Minnesota Rokkr',
           'TOR': 'Toronto Ultra',
           'ATL': 'Atlanta FaZe',
           'TX': 'OpTic Texas',
           'LAT': 'Los Angeles Thieves',
           'LAG': 'Los Angeles Guerillas',
           'SEA': 'Seattle Surge',
           'LDN': 'London Royal Ravens'}

CDL_ABBREV_FROM_NAME = {CDL_FULL_TEAM_NAMES[team]: team for team in CDL_FULL_TEAM_NAMES}

def read_matches(all=True, majors: list=None) -> pd.DataFrame:
    dfs = []
    matchIDs = pd.read_json('major_ids.json')
    
    if majors == None:
        majors = matchIDs.keys()

    for major in matchIDs:
        if major in majors:
            for setting in matchIDs[major].keys():
                try:
                    major_setting_dfs = []
                    for matchID in matchIDs[major][setting]:
                        try:
                            df = pd.read_csv(f"data/cdl_{matchID}.csv")
                        except FileNotFoundError:
                            # No data for this match
                            pass
                        major_setting_dfs.append(df)

                    major_setting_df = pd.concat(major_setting_dfs)
                    major_setting_df['event'] = f"{str(major)}_{str(setting)}"
                    major_setting_df['platform'] = 'lan' if setting == 'event' else 'online'
                    dfs.append(major_setting_df)
                except ValueError:
                    # Occurs when there are no matchIDs for the specific event
                    pass

        
    return pd.concat(dfs)

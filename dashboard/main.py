import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import utils.general as utils_gen
import utils.further_variables as fv
import utils.cdl_data_manipulation as cdl_dm
import io

SMALL_FIGURE_SIZE = (6, 4)
NORMAL_FIGURE_SIZE = (10, 6)
LARGE_FIGURE_SIZE = (14, 10)

CDL_PALLETE = utils_gen.CDL_PALETTE
CDL_PALETTE_SECONDARY = utils_gen.CDL_PALETTE_SECONDARY
CDL_FULL_TEAM_NAMES = utils_gen.CDL_FULL_TEAM_NAMES
CDL_ABBREV_FROM_NAME = {CDL_FULL_TEAM_NAMES[team]: team for team in CDL_FULL_TEAM_NAMES}

st.set_page_config(layout="wide", page_title='Team Head-to-Head')

######################################################################
#                                                                    #
#                           GRAPH THEMES                             #
#                                                                    #
######################################################################

def dark_theme(figure: plt.figure, grid:bool=False) -> None:
    for axis in figure.get_axes():

        axis.tick_params(labelcolor='white', color='white')
        axis.set_title(axis.title.get_text(), color='white')
        axis.set_facecolor("#6b7787")
        axis.spines[['right', 'top', 'left', 'bottom']].set_color('white')
        axis.set_xlabel(axis.get_xlabel(), color='white')
        axis.set_ylabel(axis.get_ylabel(), color='white')
        if grid:
            axis.grid(color='grey', alpha=0.75)

        
    figure.set_facecolor("#0c1222")
    figure.suptitle(figure._suptitle.get_text(), color='white')


def light_theme(figure: plt.figure, grid:bool=False) -> None:
    for axis in figure.get_axes():

        axis.tick_params(labelcolor='black', color='black')
        axis.set_title(axis.title.get_text(), color='black')
        axis.set_facecolor("white")
        axis.spines[['right', 'top', 'left', 'bottom']].set_color('black')
        if grid:
            axis.grid(color='grey', alpha=0.75)
        
    figure.set_facecolor("#e6e1e1")
    figure.suptitle(figure._suptitle.get_text(), color='black')


def custom_theme(figure: plt.figure, grid:bool = False) -> None:
    for axis in figure.get_axes():

        axis.tick_params(labelcolor=TERTIARY_COLOUR, color=TERTIARY_COLOUR)
        axis.set_title(axis.title.get_text(), color=TERTIARY_COLOUR)
        axis.set_facecolor(SECONDARY_COLOUR)
        axis.spines[['right', 'top', 'left', 'bottom']].set_color(TERTIARY_COLOUR)
        axis.set_xlabel(axis.get_xlabel(), color=TERTIARY_COLOUR)
        axis.set_ylabel(axis.get_ylabel(), color=TERTIARY_COLOUR)
        if grid:
            axis.grid(color=TERTIARY_COLOUR, alpha=0.75)
        
    figure.set_facecolor(PRIMARY_COLOUR)
    figure.suptitle(figure._suptitle.get_text(), color=TERTIARY_COLOUR)

def get_stack_size(base_size: tuple=NORMAL_FIGURE_SIZE, orientation: str='vertical', n: int=2) -> tuple[int, int]:
    if orientation.lower() == 'vertical':
        new_size = (base_size[0], base_size[1]*n)
    elif orientation.lower() == 'horizontal':
        new_size = (base_size[0]*n, base_size[1])
    return new_size

THEME_FUNC_MAP = {'Light': light_theme,
                   'Dark': dark_theme,
                   'Custom': custom_theme}


######################################################################
#                                                                    #
#                           GRAPH PLOTTING                           #
#                                                                    #
######################################################################


def plot_head_to_head(df, theme, selected_var):
    fig = plt.figure(figsize=(NORMAL_FIGURE_SIZE))
    axes = fig.subplots(nrows=2, sharey=True)
    for team, ax in zip(df.abbrev.unique(), axes):
        teamDF = df[df['abbrev']==team].dropna(axis=1, how='all')
        teamDF.plot(kind='bar', stacked=False, x='alias', ax=ax, color=[CDL_PALLETE[teamDF['abbrev'][0]], CDL_PALETTE_SECONDARY[teamDF['abbrev'][0]]])
        ax.set_title(f"{CDL_FULL_TEAM_NAMES[teamDF.abbrev[0]]}")
        ax.tick_params(rotation=0)
        ax.set_ylabel(selected_var)
        ax.legend(loc='lower center')
    
    teams = df.abbrev.unique()
    fig.suptitle(f"{teams[0]} vs {teams[1]} - {selected_var}")
    fig.tight_layout()
    theme(fig)
    
    return fig




######################################################################
#                                                                    #
#                      Data Filtering/Sidebar                        #
#                                                                    #
######################################################################

df = utils_gen.read_matches()
df['kd'] = df['totalKills']/df['totalDeaths']

st.sidebar.title("Graph Custimisation")
selected_theme = st.sidebar.radio('THEME', ['Light', 'Dark', 'Custom'])

if selected_theme=='Custom':
    PRIMARY_COLOUR = st.sidebar.color_picker(label='Primary Colour', help="Colour ofFigure Background\n(Double Click Color to Confirm)")
    SECONDARY_COLOUR = st.sidebar.color_picker(label="Secondary Colour", help="Colour of Individual Axis Backgrounds\n(Double Click Color to Confirm)")
    TERTIARY_COLOUR = st.sidebar.color_picker(label="TERTIARY Colour", help="Colour of Labels, Spines and Titles\n(Double Click Color to Confirm)")

st.sidebar.title("Team Selection")
team1_selectbox = st.sidebar.selectbox("Team 1",  [CDL_FULL_TEAM_NAMES[i] for i in df['abbrev'].unique()],
                                        help='The first team to include in the comparison')
team2_selectbox = st.sidebar.selectbox("Team 2", [CDL_FULL_TEAM_NAMES[i] for i in df[df['abbrev']!= CDL_ABBREV_FROM_NAME[team1_selectbox]]['abbrev'].unique()],
                                        help='The second team to include in the comparison')


st.sidebar.title("Events")
event_options = {event: st.sidebar.checkbox(event, value=True, key=i+50) for i, event in enumerate(df['event'].unique())}
selected_events = {ev for ev in event_options if event_options[ev]}

st.sidebar.title("Game Modes")
mode_options = {mode: st.sidebar.checkbox(mode, value=True, key=i+100) for i, mode in enumerate(df['gameMode'].unique())}
selected_modes = {gm for gm in mode_options if mode_options[gm]}

st.sidebar.title("Maps")
map_options = {map_: st.sidebar.checkbox(map_, value=True, key=i+150) for i, map_ in enumerate(df['gameMap'].unique())}
selected_maps = {gmap_ for gmap_ in map_options if map_options[gmap_]}

df = df[df['event'].isin(selected_events)]
df = df[df['gameMode'].isin(selected_modes)]
df = df[df['gameMap'].isin(selected_maps)]

######################################################################
#                                                                    #
#                       Grid Layout Creation                         #
#                                                                    #
######################################################################
(top_row, middle_row, bottom_row) = (st.columns(2) for i in range(3))


######################################################################
#                                                                    #
#                       DashBoard Plotting                           #
#                                                                    #
######################################################################


def background_colour_team(x):
    try:
        return f"background-color: {CDL_PALLETE[x]}"
    except:
        return None

def text_color_team(x):
    try:
        return f"color: {CDL_PALETTE_SECONDARY[x]}"
    except:
        return None

head_to_head = cdl_dm.get_head_to_head_player_stats(df, CDL_ABBREV_FROM_NAME[team1_selectbox], CDL_ABBREV_FROM_NAME[team2_selectbox])

variable_core_type = [var.replace('_vs_all', '') for var in head_to_head.select_dtypes(exclude='object').columns if '_vs_all' in var]

SELECTED_VARIABLE = top_row[0].selectbox(label="Choose Statistic", options=variable_core_type)

middle_row[0].write(head_to_head[['alias', 'abbrev', 
                                  *[var for var in head_to_head.select_dtypes(exclude='object').columns if SELECTED_VARIABLE in var]]].copy()
                                  .dropna(axis=0, how='all').reset_index(drop=True).style
                                  .format(precision=3).applymap(background_colour_team).applymap(text_color_team).background_gradient())

h2h_figure = plot_head_to_head(head_to_head[['alias', 'abbrev', 
                                  *[var for var in head_to_head.select_dtypes(exclude='object').columns if SELECTED_VARIABLE in var]]], THEME_FUNC_MAP[selected_theme],
                                  SELECTED_VARIABLE)

h2h_figure_data = io.BytesIO()
h2h_figure.savefig(h2h_figure_data, format='png')

top_row[1].download_button(
   label="Download Image as PNG",
   data=h2h_figure_data,
   file_name=f"{team1_selectbox}_vs_{team2_selectbox}_{SELECTED_VARIABLE}",
   mime="image/png"
)
middle_row[1].write(h2h_figure)





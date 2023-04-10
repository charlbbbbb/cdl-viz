import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import utils.general as utils_gen
import utils.further_variables as fv
import utils.cdl_data_manipulation as cdl_dm
import utils.cdl_graph_plotting as cgp
from utils.cdl_st_templates import light_theme, custom_theme, dark_theme, NORMAL_FIGURE_SIZE, THEME_FUNC_MAP, background_colour_team, text_color_team


CDL_PALLETE = utils_gen.CDL_PALETTE
CDL_PALETTE_SECONDARY = utils_gen.CDL_PALETTE_SECONDARY
CDL_FULL_TEAM_NAMES = utils_gen.CDL_FULL_TEAM_NAMES
CDL_ABBREV_FROM_NAME = utils_gen.CDL_ABBREV_FROM_NAME

st.set_page_config(layout="wide", page_title='Team Head-to-Head')


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

head_to_head = cdl_dm.get_head_to_head_player_stats(df, CDL_ABBREV_FROM_NAME[team1_selectbox], CDL_ABBREV_FROM_NAME[team2_selectbox])

variable_core_type = [var.replace('_vs_all', '') for var in head_to_head.select_dtypes(exclude='object').columns if '_vs_all' in var]

SELECTED_VARIABLE = top_row[0].selectbox(label="Choose Statistic", options=variable_core_type)

middle_row[0].write(head_to_head[['alias', 'abbrev', 
                                  *[var for var in head_to_head.select_dtypes(exclude='object').columns if SELECTED_VARIABLE in var]]].copy()
                                  .dropna(axis=0, how='all').reset_index(drop=True).style
                                  .format(precision=3).applymap(background_colour_team).applymap(text_color_team).background_gradient())

try:
    h2h_figure = cgp.plot_head_to_head(head_to_head[['alias', 'abbrev', 
                                    *[var for var in head_to_head.select_dtypes(exclude='object').columns if SELECTED_VARIABLE in var]]], THEME_FUNC_MAP[selected_theme],
                                    SELECTED_VARIABLE, NORMAL_FIGURE_SIZE, PRIMARY_COLOUR, SECONDARY_COLOUR, TERTIARY_COLOUR)
except NameError:
    h2h_figure = cgp.plot_head_to_head(head_to_head[['alias', 'abbrev', 
                                    *[var for var in head_to_head.select_dtypes(exclude='object').columns if SELECTED_VARIABLE in var]]], THEME_FUNC_MAP[selected_theme],
                                    SELECTED_VARIABLE, NORMAL_FIGURE_SIZE)

h2h_figure_data = io.BytesIO()
h2h_figure.savefig(h2h_figure_data, format='png')

top_row[1].download_button(
   label="Download Image as PNG",
   data=h2h_figure_data,
   file_name=f"{team1_selectbox}_vs_{team2_selectbox}_{SELECTED_VARIABLE}",
   mime="image/png"
)
middle_row[1].write(h2h_figure)





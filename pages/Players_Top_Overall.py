import streamlit as st
import pandas as pd
import io
from utils_link import utils
from utils.general import read_matches
import utils.cdl_data_manipulation as cdm
import utils.cdl_st_templates as cst
from utils.cdl_graph_plotting import plot_ranked

df = read_matches()

st.set_page_config(layout="wide", page_title='Top Overall in Stats (Player)')

st.sidebar.title("Graph Custimisation")
selected_theme = st.sidebar.radio('THEME', ['Light', 'Dark', 'Custom'])

if selected_theme=='Custom':
    PRIMARY_COLOUR = st.sidebar.color_picker(label='Primary Colour', help="Colour ofFigure Background\n(Double Click Color to Confirm)")
    SECONDARY_COLOUR = st.sidebar.color_picker(label="Secondary Colour", help="Colour of Individual Axis Backgrounds\n(Double Click Color to Confirm)")
    TERTIARY_COLOUR = st.sidebar.color_picker(label="TERTIARY Colour", help="Colour of Labels, Spines and Titles\n(Double Click Color to Confirm)")

st.sidebar.title("Team Selection")

PLAYER_COUNT = st.sidebar.slider(label="Number of Players", min_value=5, max_value=15, help="The number of players to show in the graph (e.g. top 5 and bottom 5)")

MINIMUM_MAPS =st.sidebar.slider(label="Minimum Maps Played", min_value=1, max_value=40, help="The number of maps that must be played for a player to be included")


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

(top_row, middle_row, bottom_row) = (st.columns(2) for i in range(3))

df = cdm.top_overall(df, MINIMUM_MAPS)
SELECTED_STATISTIC = top_row[0].selectbox(label="Statistic", options=[var for var in df.columns if var not in ['alias', 'abbrev']])

df = df.sort_values(SELECTED_STATISTIC, ascending=False)

max_df = df[['alias', 'abbrev', SELECTED_STATISTIC]].iloc[:PLAYER_COUNT].set_index('alias')
min_df = df[['alias', 'abbrev', SELECTED_STATISTIC]].iloc[-PLAYER_COUNT:].set_index('alias')
middle_row[0].dataframe(min_df.style.format(precision=3).reset_index().applymap(lambda x: cst.background_colour_team(x))
                 .applymap(lambda x: cst.text_color_team(x)))

middle_row[0].dataframe(max_df.style.format(precision=3).reset_index().applymap(lambda x: cst.background_colour_team(x))
                 .applymap(lambda x: cst.text_color_team(x)))

try:
    COMPUTED_FIGURE = plot_ranked(cst.THEME_FUNC_MAP[selected_theme], max_df, min_df, SELECTED_STATISTIC, True, PRIMARY_COLOUR, SECONDARY_COLOUR, TERTIARY_COLOUR)
except NameError:
    COMPUTED_FIGURE = plot_ranked(cst.THEME_FUNC_MAP[selected_theme], max_df, min_df, SELECTED_STATISTIC)
                              
top_bottom_fig = io.BytesIO()
COMPUTED_FIGURE.savefig(top_bottom_fig, format='png')

middle_row[1].write(COMPUTED_FIGURE)

top_row[1].download_button(
   label="Download Image as PNG",
   data=top_bottom_fig,
   file_name=f"{SELECTED_STATISTIC}_top_bottom_{PLAYER_COUNT}",
   mime="image/png"
)
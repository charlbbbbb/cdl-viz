import streamlit as st
import pandas as pd
import numpy as np
import io

# Local Imports -
# 'utils' need to be imported from an intermediate
# file because streamlit does not execute the 
# setup.py file

from utils_link import utils
from utils.general import read_matches
import utils.cdl_data_manipulation as cdm
import utils.cdl_st_templates as cst
from utils.cdl_graph_plotting import plot_ranked
from utils.general import CDL_FULL_TEAM_NAMES, CDL_ABBREV_FROM_NAME
from utils.further_variables import declare_map_winner, declare_match_winner, calculate_kd

df = read_matches()

st.set_page_config(layout="wide", page_title='Top Overall in Stats (Player)')

st.sidebar.title("Graph Custimisation")
selected_theme = st.sidebar.radio('THEME', ['Light', 'Dark', 'Custom'])

if selected_theme=='Custom':
    PRIMARY_COLOUR = st.sidebar.color_picker(label='Primary Colour', help="Colour ofFigure Background\n(Double Click Color to Confirm)")
    SECONDARY_COLOUR = st.sidebar.color_picker(label="Secondary Colour", help="Colour of Individual Axis Backgrounds\n(Double Click Color to Confirm)")
    TERTIARY_COLOUR = st.sidebar.color_picker(label="TERTIARY Colour", help="Colour of Labels, Spines and Titles\n(Double Click Color to Confirm)")

st.sidebar.title("Team Selection")

SELECTED_TEAM = st.sidebar.selectbox(label="Team", options=[CDL_FULL_TEAM_NAMES[x] for x in df.abbrev.unique()])
SELECTED_PLAYER = st.sidebar.selectbox(label="Player",options=df[df['abbrev']==CDL_ABBREV_FROM_NAME[SELECTED_TEAM]].alias.unique())


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
df = df[df['alias']==SELECTED_PLAYER]

df = calculate_kd(df)
df = declare_map_winner(df)
df = declare_match_winner(df)

average_map_kds = []
(top_row, middle_row, bottom_row) = (st.columns(2) for i in range(3))

def color_kd(x):
    if str(x) == 'nan':
        return "background-color:white"
    if x < 0.95:
        return "background-color:red"
    elif x > 1.05:
        return "background-color:green"
    else:
        return "background-color:orange"

def color_hillTime(x):
    if str(x) == 'nan':
        return "background-color:white"
    elif x < 30:
        return "background-color:red"
    elif x > 60:
        return "background-color:green"
    else:
        return "background-color:orange"

def color_fb(x):
    if str(x) == 'nan':
        return "background-color:white"
    elif x < 0.9:
        return "background-color:red"
    elif x > 2:
        return "background-color:green"
    else:
        return "background-color:orange"
    

map_number_df = df.groupby(['matchGame.number', 'gameMode']).mean()[['hillTime', 'kd', 'totalFirstBloodKills']].reset_index()
map_number_df["matchGame.number"] = map_number_df['matchGame.number']+1

 
map_number_df['totalFirstBloodKills'] = [og if mode == 'CDL SnD' else None for mode, og in zip(map_number_df['gameMode'], map_number_df['totalFirstBloodKills'])]

top_row[0].write(map_number_df.style.applymap(lambda x: color_kd(x), subset='kd').applymap(lambda x: color_hillTime(x), subset='hillTime').applymap(lambda x: color_fb(x), subset='totalFirstBloodKills'))
top_row[1].write(df[['hillTime', 'matchGame.number', 'matchGame.matchId']])


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
from utils.general import CDL_PALETTE, CDL_PALETTE_SECONDARY

SMALL_FIGURE_SIZE = (6, 4)
NORMAL_FIGURE_SIZE = (10, 6)
LARGE_FIGURE_SIZE = (14, 10)

def get_stack_size(base_size: tuple=NORMAL_FIGURE_SIZE, orientation: str='vertical', n: int=2) -> tuple[int, int]:
    if orientation.lower() == 'vertical':
        new_size = (base_size[0], base_size[1]*n)
    elif orientation.lower() == 'horizontal':
        new_size = (base_size[0]*n, base_size[1])
    return new_size

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


def custom_theme(PRIMARY_COLOUR, SECONDARY_COLOUR, TERTIARY_COLOUR, figure: plt.figure, grid:bool = False) -> None:
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


THEME_FUNC_MAP = {'Light': light_theme,
                   'Dark': dark_theme,
                   'Custom': custom_theme}


######################################################################
#                                                                    #
#                       DataFrame Coloring                           #
#                                                                    #
######################################################################

def background_colour_team(x):
    try:
        return f"background-color: {CDL_PALETTE[x]}"
    except:
        return None

def text_color_team(x):
    try:
        return f"color: {CDL_PALETTE_SECONDARY[x]}"
    except:
        return None
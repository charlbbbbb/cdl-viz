
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.image as image
from matplotlib.offsetbox import AnnotationBbox, OffsetImage

from utils.general import CDL_FULL_TEAM_NAMES, CDL_PALETTE, CDL_PALETTE_SECONDARY
from utils.cdl_st_templates import NORMAL_FIGURE_SIZE, get_stack_size, SMALL_FIGURE_SIZE


def plot_head_to_head(df: pd.DataFrame, theme, selected_var, figsize, col1=None, col2=None, col3=None) -> plt.figure:
    fig = plt.figure(figsize=(figsize))
    axes = fig.subplots(nrows=2, sharey=True)
    for team, ax in zip(df.abbrev.unique(), axes):
        teamDF = df[df['abbrev']==team].dropna(axis=1, how='all')
        teamDF.plot(kind='bar', stacked=False, x='alias', ax=ax, color=[CDL_PALETTE[teamDF['abbrev'][0]], CDL_PALETTE_SECONDARY[teamDF['abbrev'][0]]])
        ax.set_title(f"{CDL_FULL_TEAM_NAMES[teamDF.abbrev[0]]}")
        ax.tick_params(rotation=0)
        ax.set_ylabel(selected_var)
        ax.legend(loc='lower center')
    
    teams = df.abbrev.unique()
    fig.suptitle(f"{teams[0]} vs {teams[1]} - {selected_var}")
    fig.tight_layout()
    if col1 != None:
        theme(col1, col2, col3, fig, False)
    else:
        theme(fig)
    
    return fig

def plot_ranked(theme, df_max: pd.DataFrame, df_min : pd.DataFrame, statistic: str, player_images: bool = True, col1=None, col2=None, col3=None) -> plt.figure:
    fig = plt.figure(figsize=get_stack_size(NORMAL_FIGURE_SIZE, 'vertical', n=2))
    ax1, ax2 = fig.subplots(nrows=2)

    sns.barplot(data=df_max.reset_index(), x='alias', y=statistic, hue='abbrev', palette=CDL_PALETTE, ax=ax1, dodge=False)
    ax1.set_title(f"Top {len(df_max)} Players - {statistic}")
    
    sns.barplot(data=df_min.reset_index(), x='alias', y=statistic, hue='abbrev', palette=CDL_PALETTE, ax=ax2, dodge=False)
    ax2.set_title(f"Bottom {len(df_min)} Players - {statistic}")

    ax1.legend(bbox_to_anchor=(1, 1))
    ax2.legend(bbox_to_anchor=(1, 1))
    ax1.tick_params(rotation=45)
    ax2.tick_params(rotation=45)
    ax1.set_xlabel("")
    if player_images:
        for x, y, alias in zip(ax1.get_xticks(), df_max.reset_index()[statistic], df_max.reset_index()['alias']):
            img = image.imread(f"images/{alias}_headshot.png")
            im_box = OffsetImage(img, zoom=0.85/len(df_max))
            anno = AnnotationBbox(im_box, (x, ax1.get_ylim()[0]), frameon=False, box_alignment=(0.5, 0))
            ax1.add_artist(anno)
        
        for x, y, alias in zip(ax2.get_xticks(), df_min.reset_index()[statistic], df_min.reset_index()['alias']):
            img = image.imread(f"images/{alias}_headshot.png")
            im_box = OffsetImage(img, zoom=0.85/len(df_max))
            anno = AnnotationBbox(im_box, (x, ax2.get_ylim()[0]), frameon=False, box_alignment=(0.5, 0))
            ax2.add_artist(anno)
            
    fig.suptitle(f"Top and Bottom {len(df_min)} Players - {statistic}")
    if col1 != None:
        theme(col1, col2, col3, fig, False)
    else:
        theme(fig)
    return fig


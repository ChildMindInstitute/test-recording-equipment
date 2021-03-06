#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
recorder_box_plots.py

Functions to draw boxplots of the features with the worst parity from the data
output by openSMILE_dir_to_csv for recorder comparisons.

Author:
        – Jon Clucas, 2017 (jon.clucas@childmind.org)

© 2017, Child Mind Institute, Apache v2.0 License
"""
import os, sys
if os.path.abspath('../..') not in sys.path:
    sys.path.append(os.path.abspath('../..'))
from test_recording_equipment.utilities import cmi_color_pallette as ccp
import openSMILE_dir_to_csv as odtc, pandas as pd, matplotlib.pyplot as plt, \
       seaborn as sns, subprocess

sns.set_palette(ccp.cmi_colors())

def plot(dataframe, directory):
    dataframe = dataframe.drop(['mean', 'median', 'std', 'mad'], axis=1)
    dataframe = dataframe.T
    indices = list(dataframe.index)
    entities = []
    recorders = []
    for index in indices:
        rd, entity, recorder = index.split('_', 2)
        entities.append(entity)
        recorders.append(recorder[:-2])
    dataframe.insert(0, "entity", entities)
    dataframe.insert(0, "recorder", recorders)
    dataframe = dataframe.drop([dataframe.columns[len(dataframe.columns)-1],
                dataframe.columns[len(dataframe.columns)-2]], axis=1)
    df_long = pd.melt(dataframe, ["recorder", "entity"], var_name="features",
                      value_name="openSMILE outputs")
    print(df_long.head(140))
    plt.xticks(rotation=300, ha="left")
    plt.figsize=(22,17)
    plt.dpi=200
    g = sns.boxplot(x="features", y="openSMILE outputs", hue="recorder", data=
                    df_long.head(n=280))
    """
    plt.title(''.join(["Worst parity: ", os.path.basename(os.path.dirname(
              directory)), "/", os.path.basename(directory)]))
    """
    plt.tight_layout()
    fig = g.get_figure()
    fig.savefig(os.path.join(directory, "collected/boxplot.png"), dpi=300)
    plt.close()
    h = sns.boxplot(x="openSMILE outputs", y="features", hue="recorder", data=
                    df_long)
    h.set_aspect(28/len(df_long['features'].unique()))
    # plt.yticks(np.arange(len(df_long['features'].unique())), df_long['features'
    #           ].unique())
    # plt.tight_layout()
    fig_h = h.get_figure()
    fig_h.savefig(os.path.join(directory, "collected/horizontal_boxplot.png"), 
                  dpi=300)
    plt.close()
    
    

def main():
    tippy_top = input("Top directory for recorder test: ")
    # tippy_top = "/Users/jon.clucas/test_recording_equipment/test_equipment/recorder_test"
    top_dirs = [os.path.join(tippy_top, "sentences/ComParE_2016"),
                os.path.join(tippy_top, "sentences/emobase"),
                os.path.join(tippy_top, "word_list/ComParE_2016"),
                os.path.join(tippy_top, "word_list/emobase")]
    for directory in top_dirs:
        if os.path.exists(os.path.join(directory, ".DS_Store")):
            shell_command = ''.join(['rm ', os.path.join(directory,
                            ".DS_Store")])
            print(shell_command)
            subprocess.run(shell_command, shell = True)
        plot(odtc.oS_dir_to_csv(directory), directory)
# ============================================================================
if __name__ == '__main__':
        main()
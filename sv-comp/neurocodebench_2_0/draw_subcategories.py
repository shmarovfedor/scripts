#!/usr/bin/env python3

import sys
import pandas as pd
from collections import Counter
from matplotlib import rc
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
from matplotlib.lines import Line2D
import math
from my_constants import *
from my_utils import *


def draw_subcategory(df, filenames, shades, tool):
    #df = df[df["run_subcategory"] == subcategory]
    df = df[df["host"] == tool]

    ## plotting CPU time in the top subplot
    fig = plt.figure(figsize = (19, 8), dpi = 100)
    plt.subplot(2,1,1)

    column = "cputime"

    ## calculating min/max values for the axes
    xmin = -1
    xmax = len(filenames)
    ymax_val = df[df["run_filename_clean"].isin(filenames)][column].max()
    ymin = -0.05 * ymax_val
    ymax = 1.15 * ymax_val

    ## drawing shaded areas
    for shade in shades:
        plt.fill_between(shade, ymin, ymax, color="lightgray", label="_nolegend_")

    ## plotting the values
    i = 0
    for filename in filenames:
        value = df[df["run_filename_clean"] == filename][column]
        category = df[df["run_filename_clean"] == filename]["category"]
        reason = df[df["run_filename_clean"] == filename]["terminationreason"]
        marker = "s"
        color = "grey"
        text = "U"
        space = 0.3
        if (category == "correct").prod():
            text = "\u2714"
            #text = "T"
            color = "green"
            marker = "^"
            space = 0.5
        if (category == "wrong").prod():
            text = "\u2718"
            #text = "F"
            color = "red"
            marker = "v"
            space = 0.7
        if (category == "error").prod():
            text = "!"
            color = "darkorange"
            marker = "x"
        if (category == "unknown").prod():
            text = "?"
            color = "blue"
            marker = "o"
        if (reason == "cputime").prod():
            text = "\u2217"
            color = "black"
            marker = "x"
        if (reason == "memory").prod():
            text = "^"
            color = "black"
            marker = "s"
        #print(value.iloc[0])
        plt.text(i - space, value.iloc[0], text, color=color, fontsize=28)
        i = i + 1

    plt.xticks(range(0, len(filenames)), labels = [""] * len(filenames), rotation=90, fontsize=18)
    plt.yticks(fontsize=20)
    plt.ylabel("CPU time (s)", fontsize=24)
    plt.xlim(xmin + 0.5, xmax - 0.5)
    plt.ylim(ymin, ymax)
    plt.grid()

    ## plotting memory in the bottom subplot
    plt.subplot(2,1,2)

    column = "memory"

    ## calculating min/max values for the axes
    xmin = -1
    xmax = len(filenames)
    ymax_val = df[df["run_filename_clean"].isin(filenames)][column].max() / 1e9
    ymin = -0.05 * ymax_val
    ymax = 1.15 * ymax_val

    ## drawing shaded areas
    for shade in shades:
        plt.fill_between(shade, ymin, ymax, color="lightgray", label="_nolegend_")

    ## plotting the values
    i = 0
    for filename in filenames:
        value = df[df["run_filename_clean"] == filename][column] / 1e9
        category = df[df["run_filename_clean"] == filename]["category"]
        reason = df[df["run_filename_clean"] == filename]["terminationreason"]
        marker = "s"
        color = "grey"
        text = "U"
        space = 0.3
        if (category == "correct").prod():
            text = "\u2714"
            #text = "T"
            color = "green"
            marker = "^"
            space = 0.5
        if (category == "wrong").prod():
            text = "\u2718"
            #text = "F"
            color = "red"
            marker = "v"
            space = 0.7
        if (category == "error").prod():
            text = "!"
            color = "darkorange"
            marker = "x"
        if (category == "unknown").prod():
            text = "?"
            color = "blue"
            marker = "o"
        if (reason == "cputime").prod():
            text = "\u2217"
            color = "black"
            marker = "x"
        if (reason == "memory").prod():
            text = "^"
            color = "black"
            marker = "s"
        plt.text(i - space, value.iloc[0], text, color=color, fontsize=28)
        i = i + 1

    plt.xticks(range(0, len(filenames)), labels = filenames, rotation=90, fontsize=18)
    plt.yticks(fontsize=20)
    plt.xlabel("Benchmark name", fontsize=24)
    plt.ylabel("Memory (GB)", fontsize=24)
    plt.xlim(xmin + 0.5, xmax - 0.5)
    plt.ylim(ymin, ymax)
    plt.grid()

    plt.subplots_adjust(left=0.055, bottom=0.51, right=0.995, 
        top=0.99, wspace=0.1, hspace=0.05)
    plt.show()
    return fig


df = load_df_from_files(sys.argv[1:])
dfs = split_df_by_column(df, "data_source")
df = dfs[-1] # the last df is plain


## setting the font family
rc('font', **{'family': 'serif', 'serif': ['Linux Libertine O']})

sat_relu_shades = [[-0.5, 11.5], [23.5, 35.5], [47.5, 59.5], [71.5, 83.5]]
fig = draw_subcategory(df, SAT_RELU_ORDERED, sat_relu_shades, "esbmc")
fig.savefig("sat_relu_esbmc.pdf", format="pdf")

lipschitz_shades = [[-0.5, 17.5], [35.5, 53.5], [71.5, 89.5]]
fig = draw_subcategory(df, LIPSCHITZ_BOUNDED_ORDERED, lipschitz_shades, "esbmc")
fig.savefig("lipschitz_esbmc.pdf", format="pdf")

poly_shades = [[-0.5, 23.5], [47.5, 71.5]]
fig = draw_subcategory(df, POLY_APPROX_ORDERED, poly_shades, "esbmc")
fig.savefig("poly_esbmc.pdf", format="pdf")

hopfield_shades = [[-0.5, 7.5], [15.5, 23.5], [31.5, 39.5], [47.5, 55.5], [63.5, 71.5]]
fig = draw_subcategory(df, HOPFIELD_NETS_ORDERED, hopfield_shades, "esbmc")
fig.savefig("hopfield_esbmc.pdf", format="pdf")

sat_relu_shades = [[-0.5, 11.5], [23.5, 35.5], [47.5, 59.5], [71.5, 83.5]]
fig = draw_subcategory(df, SAT_RELU_ORDERED, sat_relu_shades, "cbmc")
fig.savefig("sat_relu_cbmc.pdf", format="pdf")

#!/usr/bin/env python3

import sys
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
from matplotlib.lines import Line2D
import math
from my_constants import *
from my_utils import *


df = load_df_from_files(sys.argv[1:])
dfs = split_df_by_column(df, "data_source")
df = dfs[-1] # the last df is plain

df = df[df["run_subcategory"] == "sat_relu"]
#df = df[df["run_subcategory"] == "lipschitz_bounded"]
#df = df[df["run_subcategory"] == "poly_approx"]
#df = df[df["run_subcategory"] == "hopfield_nets"]
df = df[df["host"] == "cbmc"]


filenames = SAT_RELU_SORTED
sat_relu_shades = [[-0.5, 11.5], [23.5, 35.5], [47.5, 59.5], [71.5, 83.5]]

#filenames = LIPSCHITZ_BOUNDED_ORDERED
#lipschitz_shades = [[-0.5, 17.5], [35.5, 53.5], [71.5, 89.5]]

#filenames = POLY_APPROX_ORDERED
#poly_shades = [[-0.5, 23.5], [47.5, 71.5]]

#filenames = HOPFIELD_NETS_ORDERED
#hopfield_shades = [[-0.5, 7.5], [15.5, 23.5], [31.5, 39.5], [47.5, 55.5], [63.5, 71.5], [79.5, 87.5]]


shades = sat_relu_shades
#shades = lipschitz_shades
#shades = poly_shades
#shades = hopfield_shades

## plotting CPU time in the top subplot
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
    if (category == "correct").prod():
        #text = "\u2714"
        text = "T"
        color = "green"
        marker = "^"
    if (category == "wrong").prod():
        #text = "\u2716"
        text = "F"
        color = "red"
        marker = "v"
    if (category == "error").prod():
        text = "!"
        color = "darkorange"
        marker = "x"
    if (category == "unknown").prod():
        text = "?"
        color = "blue"
        marker = "o"
    if (reason == "cputime").prod():
        text = "X"
        color = "black"
        marker = "x"
    if (reason == "memory").prod():
        text = "O"
        color = "black"
        marker = "s"
    #plt.scatter(i, cputime, color=color, marker=marker, s=160)
    plt.text(i - 0.4, value.iloc[0], text, color=color, fontsize=20)
    i = i + 1

plt.xticks(range(0, len(filenames)), labels = [""] * len(filenames), rotation=90, fontsize=16)
plt.yticks(fontsize=16)
#plt.xlabel("Benchmark name", fontsize=20)
plt.ylabel("CPU time (s)", fontsize=20)
plt.xlim(xmin, xmax)
plt.ylim(ymin, ymax)
plt.grid()

## plotting memory in the bottom subplot
plt.subplot(2,1,2)

column = "memory"

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
    if (category == "correct").prod():
        #text = "\u2714"
        text = "T"
        color = "green"
        marker = "^"
    if (category == "wrong").prod():
        #text = "\u2716"
        text = "F"
        color = "red"
        marker = "v"
    if (category == "error").prod():
        text = "!"
        color = "darkorange"
        marker = "x"
    if (category == "unknown").prod():
        text = "?"
        color = "blue"
        marker = "o"
    if (reason == "cputime").prod():
        text = "X"
        color = "black"
        marker = "x"
    if (reason == "memory").prod():
        text = "O"
        color = "black"
        marker = "s"
    #plt.scatter(i, cputime, color=color, marker=marker, s=160)
    plt.text(i - 0.4, value.iloc[0], text, color=color, fontsize=20)
    i = i + 1

plt.xticks(range(0, len(filenames)), labels = filenames, rotation=90, fontsize=16)
plt.yticks(fontsize=16)
plt.xlabel("Benchmark name", fontsize=20)
plt.ylabel("Memory (B)", fontsize=20)
plt.xlim(xmin, xmax)
plt.ylim(ymin, ymax)
plt.grid()

plt.subplots_adjust(left=0.055, bottom=0.52, right=0.995, 
    top=0.95, wspace=0.15, hspace=0.1)
plt.show()



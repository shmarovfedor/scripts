#!/usr/bin/env python3

import sys
import pandas as pd
from collections import Counter
from matplotlib import rc
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import math
from my_constants import *
from my_utils import *




def split_df_by_source(df):
    df_plain = df[(df["data_source"] == "plain_results/results.combined.merged.csv")][:]
    df_musl = df[(df["data_source"] == "musl_results/results.combined.merged.csv")][:]
    df_core = df[(df["data_source"] == "core_math_results/results.combined.merged.csv")][:]
    return (df_plain, df_musl, df_core)


'''
For a given verifier get a dictionary with all the benchmark names split into
the following verdicts:
   correct_true: [],
   correct_false: [],
   incorrect_true: [],
   incorrect_false: [],
   unknown: [],
   timeout: [],
   out_of_memory: [],
   other: []
'''
def get_all_stats_for_verifier(df, tool):
    res = {}
    df = df[df["host"] == tool]
    res["correct_true"] = df[(df["category"] == "correct") & 
            (df["run_expectedVerdict"] == True)]["run_filename_clean"].to_list()

    res["correct_false"] = df[(df["category"] == "correct") & 
            (df["run_expectedVerdict"] == False)]["run_filename_clean"].to_list()
    
    res["incorrect_true"] = df[(df["category"] == "wrong") & 
            (df["run_expectedVerdict"] == False)]["run_filename_clean"].to_list()
    
    res["incorrect_false"] = df[(df["category"] == "wrong") & 
            (df["run_expectedVerdict"] == True)]["run_filename_clean"].to_list()
    
    res["unknown"] = df[df["category"] == "unknown"]["run_filename_clean"].to_list()
    
    res["timeout"] = df[(df["status"] == "TIMEOUT") | 
                (df["status"] == "TIMEOUT (ERROR - no output)")]["run_filename_clean"].to_list()

    res["out_of_memory"] = df[(df["status"] == "OUT OF MEMORY") | 
                (df["status"] == "OUT OF MEMORY (ERROR - no output)")]["run_filename_clean"].to_list()

    res["other"] = df[(df["category"] == "error") 
            & ~(df["status"] == "TIMEOUT")
            & ~(df["status"] == "TIMEOUT (ERROR - no output)")
            & ~(df["status"] == "OUT OF MEMORY")
            & ~(df["status"] == "OUT OF MEMORY (ERROR - no output)")]["run_filename_clean"].to_list()
    
    return res


def plot_all_stats(df, ymax):
    (df_plain, df_musl, df_core) = split_df_by_source(df)

    formated_tool_names = {
            "2ls" : "2LS",
            "cbmc" : "CBMC",
            "cpachecker" : "CPAChecker",
            "divine" : "Divine",
            "esbmc" : "ESBMC",
            "pesco" : "PeSCo",
            "pinaka" : "Pinaka",
            "uautomizer" : "UAutomizer"}

    i = 0
    j = 1
    fig = plt.figure(figsize = (10,8), dpi=100)
    for tool in df["host"].unique():
        stats_plain = get_all_stats_for_verifier(df_plain, tool)
        stats_musl = get_all_stats_for_verifier(df_musl, tool)
        stats_core = get_all_stats_for_verifier(df_core, tool)

        plt.subplot(4, 2, j)

        text_font_size = 13
        text_vspace = 5

        # correct true
        value = len(stats_plain["correct_true"])
        plt.bar(i + 0, value, width = 1, edgecolor = "black", facecolor = "red")
        plt.text(i + 0, value + text_vspace, str(value), ha='center', fontsize=text_font_size)
        value = len(stats_musl["correct_true"])
        plt.bar(i + 1, value, width = 1, edgecolor = "black", facecolor = "blue")
        plt.text(i + 1, value + text_vspace, str(value), ha='center', fontsize=text_font_size)
        value = len(stats_core["correct_true"])
        plt.bar(i + 2, value, width = 1, edgecolor = "black", facecolor = "green")
        plt.text(i + 2, value + text_vspace, str(value), ha='center', fontsize=text_font_size)
        
        # correct false
        value = len(stats_plain["correct_false"])
        plt.bar(i + 3.5, value, width = 1, edgecolor = "black", facecolor = "red")
        plt.text(i + 3.5, value + text_vspace, str(value), ha='center', fontsize=text_font_size)
        value = len(stats_musl["correct_false"])
        plt.bar(i + 4.5, value, width = 1, edgecolor = "black", facecolor = "blue")
        plt.text(i + 4.5, value + text_vspace, str(value), ha='center', fontsize=text_font_size)
        value = len(stats_core["correct_false"])
        plt.bar(i + 5.5, value, width = 1, edgecolor = "black", facecolor = "green")
        plt.text(i + 5.5, value + text_vspace, str(value), ha='center', fontsize=text_font_size)
       
        # incorrect true
        value = len(stats_plain["incorrect_true"])
        plt.bar(i + 7, value, width = 1, edgecolor = "black", facecolor = "red")
        plt.text(i + 7, value + text_vspace, str(value), ha='center', fontsize=text_font_size)
        value = len(stats_musl["incorrect_true"])
        plt.bar(i + 8, value, width = 1, edgecolor = "black", facecolor = "blue")
        plt.text(i + 8, value + text_vspace, str(value), ha='center', fontsize=text_font_size)
        value = len(stats_core["incorrect_true"])
        plt.bar(i + 9, value, width = 1, edgecolor = "black", facecolor = "green")
        plt.text(i + 9, value + text_vspace, str(value), ha='center', fontsize=text_font_size)
        
        # incorrect false
        value = len(stats_plain["incorrect_false"])
        plt.bar(i + 10.5, value, width = 1, edgecolor = "black", facecolor = "red")
        plt.text(i + 10.5, value + text_vspace, str(value), ha='center', fontsize=text_font_size)
        value = len(stats_musl["incorrect_false"])
        plt.bar(i + 11.5, value, width = 1, edgecolor = "black", facecolor = "blue")
        plt.text(i + 11.5, value + text_vspace, str(value), ha='center', fontsize=text_font_size)
        value = len(stats_core["incorrect_false"])
        plt.bar(i + 12.5, value, width = 1, edgecolor = "black", facecolor = "green")
        plt.text(i + 12.5, value + text_vspace, str(value), ha='center', fontsize=text_font_size)
       
        legend = [
                Line2D([0], [0], marker='s', color="white", markerfacecolor='red', label='Plain', markersize=14),
                Line2D([0], [0], marker='s', color="white", markerfacecolor='blue', label='MUSL', markersize=14),
                Line2D([0], [0], marker='s', color="white", markerfacecolor='green', label='CORE-MATH', markersize=14),
                ]
        plt.legend(handles=legend, fontsize=12, ncols=3)
        plt.title(formated_tool_names[tool], fontsize=18)
        plt.xticks([1, 4.5, 8, 11.5], ["correct true", "correct false", "incorrect true", "incorrect false"], rotation=15, fontsize=14)
        plt.yticks(fontsize=14)
        plt.ylim([0, ymax])
        j = j + 1

    plt.subplots_adjust(left=0.05, bottom=0.1, right=0.95, 
            top=0.95, wspace=0.2, hspace=0.9)
    plt.show()
    return fig




## main()

# setting the font family
rc('font', **{'family': 'serif', 'serif': ['Linux Libertine O']})

df = load_df_from_files(sys.argv[1:])

# only benchmarks with math functions
df_math = df[df["run_filename_clean"].isin(BENCHMARKS_WITH_MATH)]
fig = plot_all_stats(df_math, ymax=200)
fig.savefig("math-funs.pdf", format="pdf")

# only benchmarks without math functions
df_no_math = df[~(df["run_filename_clean"].isin(BENCHMARKS_WITH_MATH))]
fig = plot_all_stats(df_no_math, ymax=500)
fig.savefig("no-math-funs.pdf", format="pdf")


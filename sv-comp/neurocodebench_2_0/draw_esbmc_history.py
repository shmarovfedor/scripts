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


def verdict_by_verifiers(df, verdict, tools):
    res = {}
    for run_name in df["run_name"].unique():
        df_run = df[df["run_name"] == run_name]
        number_of_verdicts = (df_run["category"] == verdict).sum()
        tool_names = df_run[df_run["category"] == verdict]["host"].unique()
        if (number_of_verdicts >= 1) and (set(tools).issubset(set(tool_names))):
            res[run_name] = tool_names
    return res

def verdict_by_n_verifiers(df, verdict, n):
    res = {}
    for run_name in df["run_name"].unique():
        df_run = df[df["run_name"] == run_name]
        number_of_verdicts = (df_run["category"] == verdict).sum()
        tool_names = df_run[df_run["category"] == verdict]["host"].unique()
        if number_of_verdicts == n:
            res[run_name] = tool_names
    return res


def split_df_by_source(df):
    df_plain = df[(df["data_source"] == "plain_results/results.combined.merged.csv")][:]
    df_musl = df[(df["data_source"] == "musl_results/results.combined.merged.csv")][:]
    df_core = df[(df["data_source"] == "core_math_results/results.combined.merged.csv")][:]
    return (df_plain, df_musl, df_core)


## 
# for a given verifier get a dictionary with all the benchmark names split into
# the following verdicts:
#       correct_true: [],
#       correct_false: [],
#       incorrect_true: [],
#       incorrect_false: [],
#       unknown: [],
#       timeout: [],
#       out_of_memory: [],
#       other: []
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




## main()

df = pd.DataFrame()

for arg in sys.argv[1:]:
    new_df = load_df_from_file(arg)
    new_df = add_extra_columns(new_df)
    new_df = tudy_up(new_df)
    df = pd.concat([df, new_df], ignore_index = True)


source_list = df["data_source"].to_list()
year_list = []
for source in source_list:
    year_list.append(int(source[19:23]))

df["year"] = year_list

correct_true = []
correct_false = []
incorrect_true = []
incorrect_false = []
for year in df["year"].unique():
    df_year = df[df["year"] == year]
    correct_true.append(len(df_year[(df_year["category"] == "correct") & (df_year["run_expectedVerdict"] == True)]))
    correct_false.append(len(df_year[(df_year["category"] == "correct") & (df_year["run_expectedVerdict"] == False)]))
    incorrect_true.append(len(df_year[(df_year["category"] == "wrong") & (df_year["run_expectedVerdict"] == False)]))
    incorrect_false.append(len(df_year[(df_year["category"] == "wrong") & (df_year["run_expectedVerdict"] == True)]))

years = df["year"].unique()

rc('font', **{'family': 'serif', 'serif': ['Linux Libertine O']})
fig = plt.figure(figsize = (10, 4), dpi = 100)
plt.fill_between([2023.7, 2025.5], -50, 400, color="lightgray", label="_nolegend_")
plt.text(2023.75, 175, "v1.0 release", rotation=90, fontsize = 22)
plt.plot(years, correct_true, lw = 2, marker = "s")
plt.plot(years, correct_false, lw = 2, marker = "s")
plt.plot(years, incorrect_true, lw = 2, marker = "s")
plt.plot(years, incorrect_false, lw = 2, marker = "s")
plt.legend(["correct true", "correct false", "incorrect true", "incorrect false"], fontsize = 18)
plt.xticks(fontsize = 20)
plt.xlabel("Year", fontsize = 22)
plt.yticks(fontsize = 20)
plt.ylabel("# benchmarks", fontsize = 22)
plt.xlim([2017.5, 2025.5])
plt.ylim([-20, 370])
plt.grid()
plt.subplots_adjust(left=0.09, bottom=0.2, right=0.99, 
        top=0.95, wspace=0.2, hspace=0.1)
plt.show()
fig.savefig("esbmc_history.pdf", format="pdf")



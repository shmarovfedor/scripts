#!/usr/bin/env python3

import sys
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
from collections import OrderedDict
from matplotlib.lines import Line2D
import math



## adding extra columns
def add_extra_columns(df):
    # picking the filename and the subcategory from the filepath
    df["run_filename"] = df["run_name"].apply(lambda path : path.split("/")[-1])
    df["run_filename_clean"] = df["run_filename"].apply(lambda path : path.split(".")[0])
    df["run_subcategory"] = df["run_name"].apply(lambda path : path.split("/")[-2])
    return df

## tudying up the data
def tudy_up(df):
    # removing "s" from time values and turning them into float
    df["walltime"] = df["walltime"].apply(lambda time : float(time.replace("s", "")))
    df["cputime"] = df["cputime"].apply(lambda time : float(time.replace("s", "")))
    # removing "B" from memory values and turning them into int
    df["memory"] = df["memory"].apply(lambda mem : int(mem.replace("B", "")))
    return df

## creating a DataFrame from file, and adding the "data source" column
def load_df_from_file(filepath):
    df = pd.read_csv(filepath)
    df["data_source"] = filepath
    return df




## main()

df = pd.DataFrame()

for arg in sys.argv[1:]:
    new_df = load_df_from_file(arg)
    new_df = add_extra_columns(new_df)
    new_df = tudy_up(new_df)
    df = pd.concat([df, new_df], ignore_index = True)

print(df["data_source"].unique())

# just to check whether termination reason "cputime" means a TIMEOUT
# and "memory" means OUT OF MEMORY

df_correct = df[(df["category"] == "correct")]
df_correct_true = df_correct[(df_correct["run_expectedVerdict"] == True)]
df_correct_false = df_correct[(df_correct["run_expectedVerdict"] == False)]
df_wrong = df[(df["category"] == "wrong")]
df_wrong_true = df_wrong[(df_wrong["run_expectedVerdict"] == True)]
df_wrong_false = df_wrong[(df_wrong["run_expectedVerdict"] == False)]
df_timeout = df[(df["terminationreason"] == "cputime")]
df_oom = df[(df["terminationreason"] == "memory")]


## Generating a Figure "verdicts per benchmark"
df_verdict = pd.concat([df_correct, df_wrong, df_timeout, df_oom], axis = 0)
#df_verdict_timeout_oom = pd.concat([df_correct, df_wrong, df_timeout, df_oom], axis = 0)

#print(df["run_subcategory"].unique())
#print(df_verdict)

for subcategory in df["run_subcategory"].unique():
    df_subcat = df_verdict[(df_verdict["run_subcategory"] == subcategory)].sort_values("run_filename_clean")
    labels = []
    times = []
    i = 0
    for task in df_subcat["run_filename_clean"].unique():
        labels.append(task)
        df_task = df_subcat[(df_subcat["run_filename_clean"] == task)]
        df_task = df_task.sort_values("cputime")
        new_df_task = pd.DataFrame(columns=df_task.columns)
        for data_src in df_task["data_source"].unique():
            for index, rec in df_task.iterrows():
                if(rec["data_source"] == data_src):
                    new_df_task.loc[len(new_df_task)] = rec
                    break
        df_task = new_df_task
        for index, rec in df_task.iterrows():
            # different colours for different data sources
            if (rec["data_source"] == "plain_results/results.combined.merged.csv"):
                color = "black"
            if (rec["data_source"] == "musl_results/results.combined.merged.csv"):
                color = "red"
            if (rec["data_source"] == "core_math_results/results.combined.merged.csv"):
                color = "blue"
            
            # different markers for different outcomes
            if (rec["category"] == "correct"):
                marker = "^"
            if (rec["category"] == "wrong"):
                marker = "v"
            if (rec["terminationreason"] == "cputime"):
                marker = "x"
            if (rec["terminationreason"] == "memory"):
                marker = "+"
            plt.scatter(i, math.log(rec["cputime"] + 1), color=color, marker=marker)
        i = i + 1

    legend = [
            Line2D([0], [0], marker='^', color="white", markerfacecolor='black', label='correct', markersize=9),
            Line2D([0], [0], marker='v', color="white", markerfacecolor='black', label='incorrect', markersize=9),
            Line2D([0], [0], marker='x', color="white", markeredgecolor='black', label='timeout', markersize=7),
            Line2D([0], [0], marker='+', color="white", markeredgecolor='black', label='out of memory', markersize=7),
            Line2D([0], [0], marker='s', color="white", markerfacecolor='black', label='Plain', markersize=9),
            Line2D([0], [0], marker='s', color="white", markerfacecolor='red', label='MUSL', markersize=9),
            Line2D([0], [0], marker='s', color="white", markerfacecolor='blue', label='CORE_MATH', markersize=9),
            ]

    plt.title(str("Subcategory: " + subcategory))
    plt.xlabel("Benchmark name")
    plt.ylabel("CPU time [log(time + 1)]")
    plt.xticks(range(0, len(labels)), labels = labels, rotation=90)
    plt.tight_layout()
    #plt.ylim(-30, 1000)
    plt.ylim(-1, 10)
    plt.xlim(-1, len(labels))
    plt.legend(handles=legend)
    plt.show()
    #exit()


# only final verdicts and timeouts
#df_verdict_and_timeout
